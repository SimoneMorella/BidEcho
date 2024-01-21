from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import User, Listing, Bidding, Comment, Categories
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, BiddingForm, CommentForm


# cose da fare:
# sistemare bug da not login watchlist logica in item (per riprodurlo entrare in item da not logged) sistemare con {user authenticated shit} FATTO
# dopo tutti i punti, inserire anche una lista di categorie tramite User
# e fare menu a tendina per inserire la categoria.
# inserire pagine di ricerca per categoria (pensavo a nav menu a tendina con le diverse categorie)
# fare il session per diversi user PENSO FATTO TESTARE DOPO O DOMANI FATTO
# fare la logica per piu o meno nell'add al watchlist FATTO
# logica dei bid: nuovo modello con user username, listing item, nuovo bid: nell'input del form creato da questo, ci deve stare:
# solo l'input del nuovo bid che è float e, ci deve essere il min value che è il current bid; FATTO
# se il listing item owner è lo stesso di chi sta online in quel momento allora non può biddare ma solo chiudere. FATTO
# per questo inserire invece un nuovo column nel listing chiamato active. FATTO
# active è sempre vero. Ma se l'utente owner dell'item preme il tasto closure (logica in views.item) allora active turna false FATTO
# se active turna false allora l'item scompare da active listing e compare in un altra pagina dove ci sono tutte le close listing FATTO
# nelle close listing se le apri (quindi connesse ad item) esce chi ha vinto che si prende da l'highest bid e si fa il percorso indietro per ottenere l'user, perchè ci sarà scritto chi ha vinto FATTO
# Quindi: in active false item, si cerca in bidding ( ricerca basata sull'item e l'offer) l'utente che l'ha fatta e viene displayato FATTO
# bidding form chiaramente scompare da questo in closed bid item FATTO
# se utente diverso allora posso biddare e ogni volta che biddo di piu il current_bid si aggiorna. FATTO
# logica dei commenti come logica degli item easy aggiungi e vanno sotto, modello con user, data e ora, commento; non possono essere fatti dove active è False FATTO
# finire logica commenti (manca il listare i commenti) considerando chi l'ha scritto, cosa ha scritto e quando (?) FATTO
# poi sistemare due pagine diverse tra active and close listing FATTO

def index(request):
    return render(request, "auctions/index.html", {
        "items": Listing.objects.filter(active=True),
    })

def close_listing(request):
    return render(request, "auctions/closed_listing.html", {
        "items": Listing.objects.filter(active=False),
    })

def show_categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def show_category_items(request, category_id):
    category_items = Listing.objects.filter(category=category_id, active=True)
    category_name = category_items.first().category
    return render(request, "auctions/category_items.html", {
        "category_items": category_items,
        "category_name": category_name,
    })

@login_required
def listingCreation(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "Item was added succesfully.")
            return HttpResponseRedirect(reverse("index") + "#active")
    else:
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            "form": form,
        })


def item(request, item_id, item_title):
    current_user = request.user
    listed_item_exist = Listing.objects.filter(pk=item_id, title=item_title).exists()
    if not listed_item_exist:
        return render(request, "auctions/error.html")
    listed_item = Listing.objects.get(pk=item_id, title=item_title)
    bid_form = ""
    winner = ""
    comment_form = ""
    comments = ""
    if Comment.objects.filter(item_to_comment=listed_item).exists():
        comments = Comment.objects.filter(item_to_comment=listed_item)

    if not request.user.is_anonymous:
        if listed_item in current_user.watchlist.all():
            listed_item.in_watchlist = True
        else:
            listed_item.in_watchlist = False
        
        if current_user != listed_item.owner:
            limit_bid = listed_item.current_bid + 1
            bid_form = BiddingForm(initial={"offer": limit_bid})
            bid_form.fields["offer"].widget.attrs.update({"min": limit_bid})
        
        if listed_item.active == True:
            comment_form = CommentForm()
            


    if listed_item.active == False:
        winning_bid = Bidding.objects.filter(item_bid=listed_item, offer=listed_item.current_bid)
        if winning_bid.exists():
                  winner = winning_bid.first().bidder
        else:
            winner = listed_item.owner
    print(comments)
    return render(request, "auctions/item.html", {
        "item": listed_item,
        "bid_form": bid_form,
        "is_in_watchlist": listed_item.in_watchlist,
        "winner": winner,
        "comment_form": comment_form,
        "comments": comments,
    })

@login_required
def watchlist(request):
    current_user = request.user
    watchlist_item = current_user.watchlist.all()
    print(watchlist_item)
    return render(request, "auctions/watchlist.html", {
        "w_items": watchlist_item,
    })

@login_required
def add_to_watchlist(request, item_id, item_title):
    if request.method == "POST":
        current_user = request.user
        item_to_add = Listing.objects.get(pk=item_id, title=item_title)
        if item_to_add:
            if item_to_add in current_user.watchlist.all():
                current_user.watchlist.remove(item_to_add)
                messages.success(request, "Item sucessfully removed from Watchlist")
            else:
                current_user.watchlist.add(item_to_add)
                messages.success(request, "Item sucessfully added to Watchlist")
            return HttpResponseRedirect(reverse("item", kwargs={"item_id": item_id, 
                                                                "item_title": item_title,
                                                                }))
        else:
            messages.error(request, "Item couldn't be added or removed from Watchlist")
            return HttpResponseRedirect(reverse("item", kwargs={"item_id": item_id,
                                                                "item_title": item_title,
                                                                }))
    else:
        pass

@login_required
def bid_on_item(request, item_id, item_title):
    current_user = request.user
    item_to_bid = Listing.objects.get(pk=item_id, title=item_title)
    if current_user != item_to_bid.owner:
        if request.method == "POST":
            bid_form = BiddingForm(request.POST)
            if bid_form.is_valid():
                bid_offer = bid_form.cleaned_data["offer"]
                item_to_bid.current_bid = bid_offer
                item_to_bid.save()
                Bidding.objects.create(bidder=current_user, item_bid=item_to_bid, offer=bid_offer)
                messages.success(request, "You made the biggest offer!")
            else:
                messages.error(request, "The bid didn't make it, try again bidding more than the last offer!")
            return HttpResponseRedirect(reverse("item", kwargs={"item_id": item_id,
                                                                "item_title": item_title,
                                                                }))


@login_required
def close_bid(request, item_id, item_title):
    if request.method == "POST":
        item_to_close = get_object_or_404(Listing, pk= item_id, title=item_title)
        item_to_close.active = False
        item_to_close.save()
        return HttpResponseRedirect(reverse("item", kwargs={"item_id": item_id,
                                                            "item_title": item_title,
                                                            }))


@login_required
def add_comment(request, item_id, item_title):
    current_user = request.user
    item_to_comment = get_object_or_404(Listing, pk= item_id, title=item_title)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data["text"]
            comment_object= Comment(user=current_user, item_to_comment=item_to_comment, text=comment)
            comment_object.save()
        return HttpResponseRedirect(reverse("item", kwargs={"item_id": item_id,
                                                            "item_title": item_title,
                                                            }))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
