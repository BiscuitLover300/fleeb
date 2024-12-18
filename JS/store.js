document.addEventListener('DOMContentLoaded', () => {
    const cartSidebar = document.getElementById('cart-sidebar');
    const cartItemsList = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const purchaseButton = document.getElementById('purchase-button');
    const container = document.getElementById('products');

    if (!cartSidebar || !cartItemsList || !cartTotal || !container || !purchaseButton) { //IF there is none of these variables in the html throw error 
        console.error('Some required elements are missing from the HTML.');
        return;
    }

    // Fetch products from the backend
    fetch('/products')
        .then(response => {
            if (!response.ok) { //If response is not good throw error
                throw new Error(`Failed to fetch products: ${response.statusText}`);
            }
            return response.json();
        })
        .then(products => {
            if (products.length === 0) { //If products length == 0 then no products available 
                container.innerHTML = '<p>No products available at this time.</p>';
            } else { //Otherwise grab product
                products.forEach(product => { //For each product grab their name, card, card info
                    const productCard = document.createElement('div');
                    productCard.className = 'product-card';
                    productCard.setAttribute('data-name', product.name);
                    productCard.setAttribute('data-price', product.price);

                    productCard.innerHTML = `
                        <img src="${product.image}" alt="${product.name}">
                        <h3>${product.name}</h3>
                        <p>$${product.price.toFixed(2)}</p>
                        <button class="add-to-cart">Buy Now</button>
                    `; //Displays product name & info

                    productCard.querySelector('.add-to-cart').addEventListener('click', () => { //add to cart button
                        fetch('/cart', { //fetches the product
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ name: product.name, price: product.price })
                        }).then(updateCart).catch(error => console.error('Error adding to cart:', error));//Updates the cart & catches error 
                    });

                    container.appendChild(productCard);
                });
            }
        })
        .catch(error => { //Throws error if products aren't there 
            console.error('Error fetching products:', error);
            alert('Error loading products. Please try again later.');
        });

    function updateCart() { //Updates the cart
        fetch('/cart') //fetches cart from database
            .then(response => response.json())
            .then(cart => {
                cartItemsList.innerHTML = '';
                let total = 0;

                cart.forEach(item => { //For each item in cart
                    const li = document.createElement('li'); //Create an element
                    li.textContent = `${item.name} - $${item.price.toFixed(2)} x ${item.quantity}`; //Print out item name, price, & quantity

                    const removeButton = document.createElement('button'); //Remove button
                    removeButton.textContent = 'Remove';
                    removeButton.addEventListener('click', () => { //On click of remove button
                        fetch('/cart', { //fetches & deletes from database
                            method: 'DELETE',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ name: item.name })
                        }).then(updateCart).catch(error => console.error('Error removing from cart:', error)); // Updates cart throws an error if caught
                    });

                    li.appendChild(removeButton);
                    cartItemsList.appendChild(li);
                    total += item.price * item.quantity; //Adds to total
                });

                cartTotal.textContent = total.toFixed(2);
                purchaseButton.style.display = cart.length > 0 ? 'block' : 'none'; //If cart length is 0 do not display proceed to checkout button
                cartSidebar.classList.toggle('open', cart.length > 0); // Opens the cartsidebar if no other issues
            })
            .catch(error => console.error('Error fetching cart:', error)); //Throws error if there is one catching the 
    }

    purchaseButton.addEventListener('click', () => { //Purchase button
        alert('Proceeding to checkout...');
        window.location.href = 'checkout.html';
    });

    updateCart(); //Updates cart
});