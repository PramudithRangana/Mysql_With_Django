document.addEventListener('DOMContentLoaded', () => {
    // Generic function to enable column hovering for headers only
    function enableColumnHover(tableSelector) {
        const tables = document.querySelectorAll(tableSelector);

        tables.forEach(table => {
            table.addEventListener('mouseover', (e) => {
                // Ensure the event is triggered only on the table header (<thead>)
                const isHeader = e.target.closest('thead');
                if (isHeader && (e.target.tagName === 'TD' || e.target.tagName === 'TH')) {
                    const column = e.target.getAttribute('data-column');
                    if (column) {
                        const cells = table.querySelectorAll(`[data-column="${column}"]`);
                        cells.forEach(cell => cell.classList.add('hover-column'));
                    }
                }
            });

            table.addEventListener('mouseout', (e) => {
                const isHeader = e.target.closest('thead');
                if (isHeader && (e.target.tagName === 'TD' || e.target.tagName === 'TH')) {
                    const column = e.target.getAttribute('data-column');
                    if (column) {
                        const cells = table.querySelectorAll(`[data-column="${column}"]`);
                        cells.forEach(cell => cell.classList.remove('hover-column'));
                    }
                }
            });
        });
    }

    // Apply the function to all tables with the class 'hoverable-table'
    enableColumnHover('.hoverable-table');
});
