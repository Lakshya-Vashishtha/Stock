$(document).ready(function () {
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
     */
const fetchDashboardData = async () => {
    // Show loading spinners on all relevant sections
    loadingSpinners.removeClass('d-none');

    try {
        const response = await fetch('/api/dashboard_data', {
            credentials: 'include'  // <== important!
        });

        console.log("Response status:", response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();  // ✅ Only once!
        console.log("Dashboard data:", data);

        // Update UI elements with data from the response
        shopNameElem.text(data.shopName || 'N/A');
        userNameElem.text(data.userName || 'User');
        userBusinessTypeElem.text(data.userBusinessType || 'N/A');
        totalProductsElem.text(data.totalProducts?.toLocaleString() || '0');
        monthlySalesElem.text(`₹${(data.monthlySales || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
        totalBrandsElem.text(data.totalBrands?.toLocaleString() || '0');
        lowStockItemsElem.text(data.lowStockItems?.toLocaleString() || '0');

        // TODO: Update recentProducts and topProducts if needed

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
});