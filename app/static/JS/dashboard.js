
<old_str>$(document).ready(function () {
    // --- Element Selectors ---
    const shopNameElem = $('#shopName');
    const userNameElem = $('#userName');
    const userBusinessTypeElem = $('#userBusinessType');
    const totalProductsElem = $('#totalProducts');
    const monthlySalesElem = $('#monthlySales');
    const totalBrandsElem = $('#totalBrands');
    const lowStockItemsElem = $('#lowStockItems');
    const alertContainer = $('#alert-container');
    const loadingSpinners = $('.loading-spinner');

    /**
     * Shows an alert message to the user in the alert container.
     * @param {string} message - The message to display.
     * @param {string} [type='danger'] - The alert type (e.g., 'success', 'danger', 'warning').
     */
    function showAlert(message, type = 'danger') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
        // Replace any existing alert with the new one.
        alertContainer.html(alertHtml);
    }

    /**
     * Fetches data from the dashboard API and updates the UI.
     */</old_str>
<new_str>$(document).ready(function () {
    // --- Element Selectors ---
    const shopNameElem = $('#shopName');
    const userNameElem = $('#userName');
    const userBusinessTypeElem = $('#userBusinessType');
    const totalProductsElem = $('#totalProducts');
    const monthlySalesElem = $('#monthlySales');
    const totalBrandsElem = $('#totalBrands');
    const lowStockItemsElem = $('#lowStockItems');
    const recentProductsElem = $('#recentProducts');
    const topProductsElem = $('#topProducts');
    const alertContainer = $('#alert-container');
    const loadingSpinners = $('.loading-spinner');

    /**
     * Shows an alert message to the user in the alert container.
     * @param {string} message - The message to display.
     * @param {string} [type='danger'] - The alert type (e.g., 'success', 'danger', 'warning').
     */
    function showAlert(message, type = 'danger') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
        // Replace any existing alert with the new one.
        alertContainer.html(alertHtml);
    }

    /**
     * Fetches data from the dashboard API and updates the UI.
     */
    const fetchDashboardData = async () => {
        // Show loading spinners on all relevant sections
        loadingSpinners.removeClass('d-none');

        try {
            const response = await fetch('/api/dashboard_data', {
                credentials: 'include'
            });

            console.log("Response status:", response.status);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Dashboard data:", data);

            // Update UI elements with data from the response
            shopNameElem.text(data.shopName || 'N/A');
            userNameElem.text(data.userName || 'User');
            userBusinessTypeElem.text(data.userBusinessType || 'N/A');
            totalProductsElem.text(data.totalProducts?.toLocaleString() || '0');
            monthlySalesElem.text(`₹${(data.monthlySales || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
            totalBrandsElem.text(data.totalBrands?.toLocaleString() || '0');
            lowStockItemsElem.text(data.lowStockItems?.toLocaleString() || '0');

            // Update recent products table
            if (data.recentProducts && data.recentProducts.length > 0) {
                let productsHtml = '';
                data.recentProducts.forEach(product => {
                    productsHtml += `
                        <tr>
                            <td>${product.name || 'N/A'}</td>
                            <td>${product.brand || 'N/A'}</td>
                            <td>${product.category || 'N/A'}</td>
                            <td>${product.stock_level || 0}</td>
                            <td>₹${(product.price || 0).toFixed(2)}</td>
                            <td>${product.expiry_date || 'N/A'}</td>
                        </tr>
                    `;
                });
                recentProductsElem.html(productsHtml);
            } else {
                recentProductsElem.html('<tr><td colspan="6" class="text-center">No products found</td></tr>');
            }

            // Update top products (showing top 5 by stock level)
            if (data.recentProducts && data.recentProducts.length > 0) {
                const topProducts = data.recentProducts
                    .sort((a, b) => b.stock_level - a.stock_level)
                    .slice(0, 5);
                
                let topProductsHtml = '';
                topProducts.forEach(product => {
                    topProductsHtml += `
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            ${product.name}
                            <span class="badge bg-primary rounded-pill">${product.stock_level}</span>
                        </li>
                    `;
                });
                topProductsElem.html(topProductsHtml);
            } else {
                topProductsElem.html('<li class="list-group-item text-center">No products found</li>');
            }

        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
            showAlert('Failed to load dashboard data. Please check your connection and try again.');
        } finally {
            // Hide loading spinners after the fetch is complete
            loadingSpinners.addClass('d-none');
        }
    };

    // Initial fetch when the page loads
    fetchDashboardData();

    // Logout functionality
    $('#logoutBtn').on('click', function(e) {
        e.preventDefault();
        window.location.href = '/logout';
    });
});</old_str>
