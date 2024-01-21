// elements for category page
catBtns = document.querySelectorAll(".category-btn");
categoryImgBox = document.querySelector(".category-img");
categoryTextBox = document.querySelector(".category-text");
spanBox = document.querySelector(".category-name");
goBtn = document.querySelector(".category-link");

// elements for active listing page
rowBtns = document.querySelectorAll(".row-btn");
rowItems = document.querySelectorAll(".item");
itemsPrices = document.querySelectorAll(".item-bid");
itemsImages = document.querySelectorAll(".active-listing .items-container .item .item-img-box img");
itemsTitles = document.querySelectorAll(".active-listing .items-container .item .item-info-box .title-category");
itemsCategories = document.querySelectorAll(".active-listing .items-container .item .item-info-box .title-category .item-category");


// nav responsive elements
menuIcon = document.querySelector(".menu-icon");
dropdownNav = document.querySelector(".dropdown-menu");

menuIcon.addEventListener("click", (e)=> {
    // dropdownNav.classList.toggle("dropdown-off");
    dropdownNav.classList.toggle("dropdown-on");
})

function addImageAndText (button, imgBox, textBox) {
    buttonData = button.textContent.trim();
    console.log(buttonData);
    let src = "";
    let text = "";
    let link = "";
    switch (buttonData) {
        case ("Electronics"):
            src = "/static/auctions/category/electronics.png";
            text = "Latest smartphones, high-performance laptops, versatile tablets, and hi-tech smartwatches.";
            link = "categories/1";
            break
        case ("Fashion and Apparel"):
            src = "/static/auctions/category/fashion.png";
            text = "Designer dresses, luxury handbags, stylish footwear, and fashionable accessories.";
            link = "categories/2";
            break
        case ("Home and Garden"):
            src = "/static/auctions/category/garden.png";
            text = "Decorative vases, outdoor furniture, gardening tools, and home lighting.";
            link = "categories/3";
            break
        case ("Collectibles and Art"):
            src = "/static/auctions/category/collectibles.png";
            text = "Vintage coins, antique stamps, sculptures, and classic paintings.";
            link = "categories/4";
            break
        case("Toys and Hobbies"):
            src = "/static/auctions/category/toys.png";
            text ="Model trains, action figures, board games, and remote-controlled vehicles.";
            link = "categories/5";
            break
        case("Automotive"):
            src = "/static/auctions/category/automotive.png";
            text = "Classic car models, automotive parts, car care products, and high-tech accessories.";
            link = "categories/6";
            break
        case("Health and Beauty"):
            src = "/static/auctions/category/health.png";
            text = "Premium skincare, makeup sets, luxury fragrances, and wellness supplements.";
            link = "categories/7";
            break
        case("Sports and Outdoors"):
            src = "/static/auctions/category/sports.png";
            text = "Athletic gear, camping equipment, bicycles, and fishing gear.";
            link = "categories/8";
            break
        case("Books, Movies and Music"):
            src = "/static/auctions/category/books.png";
            text = "Bestselling books, classic film reels, vinyl records, and music CDs.";
            link = "categories/9";
            break
    }
    if (imgBox.querySelector("img") === null) {
        let img = document.createElement("img");
        imgBox.append(img);
    }
    console.log(goBtn);
    let image = imgBox.querySelector("img");
    image.setAttribute("src", src);
    image.setAttribute("alt", "category image");
    spanBox.textContent = buttonData;
    textBox.textContent = text;
    goBtn.removeAttribute('hidden');
    goBtn.setAttribute('href', link);

}

function changeItemsInRows (filterButton, items, prices) {
    let itemsInRows = filterButton.textContent;
    switch (itemsInRows) {
        case ("3"):
            items.forEach((item) => {
                item.style.width = 'calc(71vw / 3)'
            });
            prices.forEach((price) => {
                price.style.fontSize = '1.3rem'
            });
            itemsImages.forEach((image) => {
                image.style.height = "230px"
            });
            itemsTitles.forEach((title) => {
                title.style.fontSize = "1rem"
            });
            itemsCategories.forEach((category) => {
                category.style.fontSize = "0.6rem"
            });
            break
        case ("4"):
            items.forEach((item) => {
                item.style.width = 'calc(71vw / 4)'
            });
            prices.forEach((price) => {
                price.style.fontSize = '1rem'
            });
            itemsImages.forEach((image) => {
                image.style.height = "190px"
            });
            itemsTitles.forEach((title) => {
                title.style.fontSize = "0.9rem"
            });
            itemsCategories.forEach((category) => {
                category.style.fontSize = "0.5rem"
            });
            break
        case ("5"):
            items.forEach((item) => {
                item.style.width = 'calc(71vw / 5)'
            });
            prices.forEach((price) => {
                price.style.fontSize = '0.85rem'
            });
            itemsImages.forEach((image) => {
                image.style.height = "150px"
            });
            itemsTitles.forEach((title) => {
                title.style.fontSize = "0.80rem"
            });
            itemsCategories.forEach((category) => {
                category.style.fontSize = "0.45rem"
            });
            break
    }
}

catBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
        addImageAndText(btn, categoryImgBox, categoryTextBox);
    })
})

rowBtns.forEach((rowbtn) => {
    rowbtn.addEventListener("click", (e) => {
        changeItemsInRows(rowbtn, rowItems, itemsPrices);
    })
})