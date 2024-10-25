// Execute function for Initial page load 
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('searchfilter').classList.add('hidden');
    retrieveDishes()
});
// Pagination
let currentPage = 1;
let minPage;
let maxPage;
// Search, Filter, DebounceCallBack
let debounceTimeout;
let category = "";
let dish_name = "";
let min_price = "";
let max_price = "";
let sort_by = "";
// Store restaurants image url
let restaurantsImageUrl = []

// Searching and Filter Logic
function setDishName(newDishName) {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
        if (dish_name !== newDishName) {
            dish_name = newDishName;
            retrieveDishes();
        }
    }, 1000);
}
function setMinPrice(newMinPrice) {
    min_price = newMinPrice;

    // Update input di filter bar
    const filterBarMinPrice = document.getElementById('minPriceInput');
    if (filterBarMinPrice) {
        filterBarMinPrice.value = newMinPrice;
    }

    // Update input di modal
    const modalMinPrice = document.getElementById('modalMinPrice');
    if (modalMinPrice) {
        modalMinPrice.value = newMinPrice;
    }
}
function setMaxPrice(newMaxPrice) {
    max_price = newMaxPrice;

    // Update input di filter bar
    const filterBarMaxPrice = document.getElementById('maxPriceInput');
    if (filterBarMaxPrice) {
        filterBarMaxPrice.value = newMaxPrice;
    }

    // Update input di modal
    const modalMaxPrice = document.getElementById('modalMaxPrice');
    if (modalMaxPrice) {
        modalMaxPrice.value = newMaxPrice;
    }
}
function setSortBy(newSortBy) {
    sort_by = newSortBy;

    // Update select dropdown di filter bar
    const filterBarSortBy = document.querySelector('select[name="sort_by"]');
    if (filterBarSortBy) {
        filterBarSortBy.value = newSortBy;
    }

    // Update select dropdown di modal
    const modalSortBy = document.getElementById('modalSortBy');
    if (modalSortBy) {
        modalSortBy.value = newSortBy;
    }

    retrieveDishes();
}
function setCategory(newCategory) {
    // Toggle behavior for radio buttons
    if (category === newCategory) {
        // If the selected category is clicked again, deselect it
        category = "";
        // Uncheck the selected radio button
        const selectedRadio = document.querySelector(`input[name="category"][value="${newCategory}"]`);
        if (selectedRadio) {
            selectedRadio.checked = false;
        }
    } else {
        // Otherwise, set the new category
        category = newCategory;

        // Update input radio in filter bar
        const filterBarCategoryRadio = document.querySelector(`input[name="category"][value="${newCategory}"]`);
        if (filterBarCategoryRadio) {
            filterBarCategoryRadio.checked = true;
        }

        // Update input radio in modal
        const modalCategoryRadio = document.querySelector(`input[name="modalCategory"][value="${newCategory}"]`);
        if (modalCategoryRadio) {
            modalCategoryRadio.checked = true;
        }
    }

    // Refresh dishes with the new category
    retrieveDishes();
}
// Additional Function for price
function resetPriceRange() {
    document.getElementById('minPriceInput').value = '';
    document.getElementById('maxPriceInput').value = '';
    min_price = '';
    max_price = '';
}
function submitPriceRange() {
    if (parseInt(min_price) > parseInt(max_price)) {
        alert("Min Price cannot be greater than Max Price.");
        return;
    }

    // If everything is valid, proceed to retrieve the data
    retrieveDishes();
}
// Communicate with Back-End using Post Method
async function getDishes() {
    const response = await fetch(getDishesUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')  // Menambahkan CSRF token
        },
        body: JSON.stringify({
            'name': dish_name,
            'category': category,
            'price_min': min_price,
            'price_max': max_price,
            'sort_by': sort_by,
            'page' : currentPage,
        }),
    });

    if (response.ok) {
        return response.json();
    }
}
// Communicate with Back-End using GET method
async function getMoreDishes() {
    // Membuat query string dari parameter yang ada
    const queryParams = new URLSearchParams({
        'name': dish_name,
        'category': category,
        'price_min': min_price,
        'price_max': max_price,
        'sort_by': sort_by,
        'page': currentPage
    }).toString();
    
    // Menggabungkan URL dengan query string
    const urlWithParams = `${getDishesUrl}?${queryParams}`;

    const response = await fetch(urlWithParams, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')  // Menambahkan CSRF token
        }
    });

    if (response.ok) {
        return response.json();
    }
}
// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Get on Refresh and Get More Data
async function retrieveDishes() {
    buildSkeletonCards()

    // The real loading (fetching data from API)
    currentPage = 1 // initial data from start 
    const data = await getDishes();

    // Store data
    const dishes = data.dishes;

    minPage = data.min_page;
    maxPage = data.max_page;

    // Process data of producst into html string
    classNameString = "";
    htmlString = "";

    document.getElementById('searchfilter_skeleton').classList.add('hidden');
    document.getElementById('searchfilter').classList.remove('hidden');
    if (dishes.length === 0) {
        buildNoData()
    } else {
        buildCards(dishes)
    }   

}
async function retrieveMoreDishes() {
    // The real loading (fetching data from API)
    const data = await getMoreDishes();

    // Store data
    const dishes = data.dishes;

    // Process data of producst into html string
    buildCards(dishes)
}
// Build UI Components
function buildSkeletonCards() {
    classNameString = ""
    htmlString = ""
    // Loading indicator is viewing Skeleton Card
    classNameString = "mx-5 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5 justify-items-center"
    for (var i = 0 ; i < 15 ; i++) {
        htmlString += `
            <div class="relative group flex justify-center w-full">
                <!-- Skeleton Card -->
                <div class="shadow-yellow-600 shadow-2xl relative w-full h-0 pb-[80%] cursor-pointer bg-gray-200 animate-fast-pulse rounded-lg"></div>
            
                <!-- Skeleton Overlay (Popover) -->
                <div class="absolute w-full h-0 pb-[80%] bg-gray-800 opacity-0 group-hover:opacity-100 transition-all duration-300 ease-in-out transform group-hover:scale-110 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col z-10 group-hover:z-50 rounded-lg animate-fast-pulse">
                    <div class="relative w-full h-0 pb-[80%] bg-gray-300 rounded-lg"></div>
            
                    <!-- Skeleton Pre-Detail Overlay -->
                    <div class="absolute bottom-0 left-0 w-full p-2 bg-gray-700 bg-opacity-60 rounded-b-lg">
                        <div class="h-4 bg-gray-400 rounded w-3/4 mb-2"></div>
                        <div class="h-3 bg-gray-400 rounded w-1/2 mb-1"></div>
            
                        <!-- Skeleton Price and Rating -->
                        <div class="flex flex-row justify-between">
                            <div class="h-3 bg-gray-400 rounded w-1/4"></div>
                            <div class="flex items-center mt-1 justify-end space-x-1">
                                <!-- Skeleton stars -->
                                <div class="w-3 h-3 bg-gray-400 rounded-full"></div>
                                <div class="w-3 h-3 bg-gray-400 rounded-full"></div>
                                <div class="w-3 h-3 bg-gray-400 rounded-full"></div>
                                <div class="w-3 h-3 bg-gray-400 rounded-full"></div>
                                <div class="w-3 h-3 bg-gray-400 rounded-full"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }
    document.getElementById("dish_list_view").innerHTML = htmlString;
    document.getElementById("dish_list_view").className = classNameString;
}
function buildNoData() {
    classNameString = "flex flex-col items-center justify-center h-64";
    htmlString = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2a10 10 0 100 20 10 10 0 000-20zm-2 14h4m-4-8h.01M16.5 8.5a.5.5 0 11-.5-.5.5.5 0 01.5.5zm-9 0a.5.5 0 11-.5-.5.5.5 0 01.5.5z"/>
        </svg>
        <p>Can't find anything</p>
    `;
    document.getElementById("dish_list_view").innerHTML = htmlString;
    document.getElementById("dish_list_view").className = classNameString;
}
function buildCards(dishes) {
    classNameString = 'mx-5 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5 justify-items-center';
    dishes.forEach((item) => {
        let photoSectionOnItemHtmlString = "";
        let photoSectionOnModalHtmlString = ""
        if (item.image) {
            photoSectionOnItemHtmlString = `<img src="${ item.image }" class="absolute top-0 left-0 w-full h-full object-cover rounded-lg group-hover:opacity-80">`
            photoSectionOnModalHtmlString = `<img src="${ item.image }" class="absolute top-0 left-0 w-full h-full object-cover rounded-lg">`
        } else {
            photoSectionOnItemHtmlString = `
                <div class="absolute top-0 left-0 w-full h-full bg-gray-200 flex items-center justify-center rounded-lg">
                    <svg class="w-16 h-16 text-gray-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm11.707 6.707l-3 3a1 1 0 01-1.414 0l-1.586-1.586a1 1 0 00-1.414 0l-3 3A1 1 0 015 11.293l3-3a1 1 0 011
                        .414 0l1.586 1.586a1 1 0 001.414 0l3-3a1 1 0 011.414 1.414z"/>
                    </svg>
                </div>
            `;
            photoSectionOnModalHtmlString = `
                <div class="absolute top-0 left-0 w-full h-full bg-gray-200 flex items-center justify-center rounded-lg">
                    <svg class="w-16 h-16 text-gray-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm11.707 6.707l-3 3a1 1 0 01-1.414 0l-1.586-1.586a1 1 0 00-1.414 0l-3 3A1 1 0 015 11.293l3-3a1 1 0 011.414 0l1.586 1.586a1 1 0 001.414 0l3-3a1 1 0 011.414 1.414z"/>
                    </svg>
                </div>
            `;
        }

        htmlString += `
            <div class="relative group flex justify-center w-full">
                <a class="shadow-yellow-600 shadow-2xl relative w-full h-0 pb-[80%] cursor-pointer transition duration-200" href="">
                    ${photoSectionOnItemHtmlString}
                    <div class="absolute bottom-0 left-0 w-full bg-black bg-opacity-50 text-white p-2 rounded-b-lg">
                        <h3 class="font-semibold truncate">${ item.name }</h3>
                    </div>
                </a>
                <a class="absolute w-full h-0 pb-[80%] bg-gray-800 text-white opacity-0 group-hover:opacity-100 transition-all duration-300 ease-in-out transform group-hover:scale-110 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col z-10 group-hover:z-50 rounded-lg" href="">
                    <div class="relative w-full h-0 pb-[80%]">
                        ${photoSectionOnModalHtmlString}
                        <div class="absolute bottom-0 left-0 w-full text-white p-2 rounded-b-lg bg-gradient-to-t from-black via-black/60">
                            <h3 class="font-semibold truncate">${ item.name }</h3>
                            <p class="text-xs text-gray-300 line-clamp-2">${ item.description }</p>
                            <div class="flex flex-row justify-between">
                                <p class="text-xs font-semibold text-white mt-2"><strong>Price:</strong> Rp.${ item.price }</p>
                                <div class="flex items-center mt-1 justify-end">
                                    <!-- Assuming rating is coming as part of the item -->
                                       ${[...Array(5)].map((_, i) => `<svg class="w-3 h-3 ${i < item.average_rating ? 'text-yellow-400' : 'text-gray-300'}" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.049 2.927C9.22 2.613 9.58 2.454 9.955 2.454c.374 0 .736.159.907.474l2.318 4.693 5.195.756c.378.055.707.294.876.638.169.345.14.75-.076 1.086l-3.762 3.669.889 5.18c.066.385-.094.779-.414 1.017-.32.239-.748.292-1.117.138l-4.656-2.448-4.656 2.448c-.369.154-.797.1-1.117-.138-.32-.238-.48-.632-.414-1.017l.889-5.18-3.762-3.669c-.217-.336-.245-.741-.076-1.086.17-.344.498-.583.876-.638l5.195-.756L9.049 2.927z"/></svg>`).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
        `;
    });
    document.getElementById("dish_list_view").innerHTML = htmlString;
    document.getElementById("dish_list_view").className = classNameString;
}
// Toggle modal visibility
function toggleModal() {
    const modal = document.getElementById('filterModal');
    modal.classList.toggle('hidden');
    modal.classList.toggle('flex');
}
// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('filterModal');
    if (event.target == modal) {
        toggleModal();
    }
}
// When Reach Bottom add More Products
window.addEventListener ('scroll', async () => {
    const {
        scrollTop,
        scrollHeight,
        clientHeight
    } = document.documentElement;
    if (scrollTop + clientHeight >= scrollHeight - 200 &&
        currentPage <= maxPage
    ) {
        currentPage += 1
        await retrieveMoreDishes();
    }
});