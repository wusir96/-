/**
 * 医院信息管理系统前端脚本
 */

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {

    // 表格行悬停效果
    initTableHover();

    // 删除确认
    initDeleteConfirmation();

    // 设置当前导航项为活动状态
    setActiveNavItem();

    // 表单验证
    initFormValidation();

    // 消息自动消失
    initAlertDismiss();

    // 初始化工具提示
    initTooltips();

    // 初始化药品搜索
    initMedicineSearch();

    // 初始化处方计算功能
    initPrescriptionCalculator();

    // 初始化日期选择器
    initDatePickers();

    // 初始化打印功能
    initPrintButtons();

    // 初始化图表(如果页面有图表)
    initCharts();
});

/**
 * 初始化表格行悬停效果
 */
function initTableHover() {
    const tableRows = document.querySelectorAll('table tbody tr');
    if (tableRows.length > 0) {
        tableRows.forEach(row => {
            row.addEventListener('mouseover', function() {
                this.classList.add('table-hover');
            });
            row.addEventListener('mouseout', function() {
                this.classList.remove('table-hover');
            });
        });
    }
}

/**
 * 初始化删除确认对话框
 */
function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                const itemName = this.dataset.itemName || '这条记录';
                if (!confirm(`确定要删除${itemName}吗？此操作不可恢复。`)) {
                    event.preventDefault();
                }
            });
        });
    }
}

/**
 * 设置当前导航项为活动状态
 */
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });
}

/**
 * 初始化表单验证
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    if (forms.length > 0) {
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }
}

/**
 * 初始化消息自动消失
 */
function initAlertDismiss() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    if (alerts.length > 0) {
        alerts.forEach(alert => {
            setTimeout(() => {
                // 添加淡出效果
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 3000);
        });
    }
}

/**
 * 初始化Bootstrap工具提示
 */
function initTooltips() {
    // 检查是否已加载Bootstrap的tooltip组件
    if (typeof bootstrap !== 'undefined' && typeof bootstrap.Tooltip !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * 初始化药品搜索功能
 */
function initMedicineSearch() {
    const searchInput = document.getElementById('medicine-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const rows = document.querySelectorAll('table tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }
}

/**
 * 初始化处方计算器
 */
function initPrescriptionCalculator() {
    const quantityInputs = document.querySelectorAll('.prescription-quantity');
    if (quantityInputs.length > 0) {
        quantityInputs.forEach(input => {
            input.addEventListener('change', updatePrescriptionTotal);
        });

        // 初始计算总价
        updatePrescriptionTotal();
    }
}

/**
 * 更新处方总价
 */
function updatePrescriptionTotal() {
    const detailRows = document.querySelectorAll('.prescription-detail-row');
    let total = 0;

    detailRows.forEach(row => {
        const quantity = parseFloat(row.querySelector('.prescription-quantity').value) || 0;
        const price = parseFloat(row.querySelector('.prescription-price').textContent) || 0;
        const subtotal = quantity * price;

        // 更新小计显示
        const subtotalElement = row.querySelector('.prescription-subtotal');
        if (subtotalElement) {
            subtotalElement.textContent = subtotal.toFixed(2);
        }

        total += subtotal;
    });

    // 更新总计显示
    const totalElement = document.getElementById('prescription-total');
    if (totalElement) {
        totalElement.textContent = total.toFixed(2);
    }

    // 如果有隐藏字段，也更新它
    const totalAmountInput = document.getElementById('total_amount');
    if (totalAmountInput) {
        totalAmountInput.value = total.toFixed(2);
    }
}

/**
 * 初始化日期选择器
 */
function initDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    if (dateInputs.length > 0) {
        dateInputs.forEach(input => {
            // 为没有值的日期输入框设置默认值为今天
            if (input.classList.contains('date-today') && !input.value) {
                const today = new Date();
                const year = today.getFullYear();
                let month = today.getMonth() + 1;
                month = month < 10 ? '0' + month : month;
                let day = today.getDate();
                day = day < 10 ? '0' + day : day;
                input.value = `${year}-${month}-${day}`;
            }
        });
    }
}

/**
 * 初始化打印按钮
 */
function initPrintButtons() {
    const printButtons = document.querySelectorAll('.print-btn');
    if (printButtons.length > 0) {
        printButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();

                // 准备打印区域
                const printArea = document.querySelector(this.dataset.printTarget) || document;

                // 添加打印样式，如果需要
                document.body.classList.add('printing');

                // 打印
                window.print();

                // 移除打印样式
                document.body.classList.remove('printing');
            });
        });
    }
}

/**
 * 初始化统计图表
 */
function initCharts() {
    const chartElements = document.querySelectorAll('.chart-container');

    // 如果页面上有图表容器但没有加载Chart.js，输出警告
    if (chartElements.length > 0 && typeof Chart === 'undefined') {
        console.warn('页面包含图表容器，但Chart.js未加载');
        return;
    }

    // 如果有图表元素且加载了Chart.js，初始化图表
    if (chartElements.length > 0 && typeof Chart !== 'undefined') {
        chartElements.forEach(container => {
            const canvas = container.querySelector('canvas');
            const type = container.dataset.chartType || 'bar';
            const endpoint = container.dataset.chartEndpoint;

            if (canvas && endpoint) {
                // 从API获取数据
                fetch(endpoint)
                    .then(response => response.json())
                    .then(data => {
                        new Chart(canvas, {
                            type: type,
                            data: data,
                            options: {
                                responsive: true,
                                maintainAspectRatio: false
                            }
                        });
                    })
                    .catch(error => console.error('获取图表数据失败:', error));
            }
        });
    }
}

/**
 * 库存预警检查
 */
function checkLowStock() {
    const stockElements = document.querySelectorAll('.stock-level');

    if (stockElements.length > 0) {
        stockElements.forEach(element => {
            const stock = parseInt(element.textContent);
            const threshold = parseInt(element.dataset.threshold || 10);

            if (stock <= threshold) {
                element.classList.add('text-danger', 'fw-bold');
                element.setAttribute('data-bs-toggle', 'tooltip');
                element.setAttribute('title', '库存低，请及时补充');
            }
        });

        // 初始化工具提示
        initTooltips();
    }
}

/**
 * 过滤表格数据
 * @param {string} inputId - 输入框ID
 * @param {string} tableId - 表格ID
 */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    if (input && table) {
        input.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }
}

/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 * @param {Element} button - 触发复制的按钮
 */
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text)
        .then(() => {
            const originalText = button.textContent;
            button.textContent = '已复制!';
            button.classList.add('btn-success');
            button.classList.remove('btn-secondary');

            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-secondary');
            }, 2000);
        })
        .catch(err => {
            console.error('复制失败:', err);
            alert('复制失败，请手动复制');
        });
}

/**
 * 动态添加处方药品行
 */
document.addEventListener('DOMContentLoaded', function() {
    const addDetailButton = document.getElementById('add-prescription-detail');
    if (addDetailButton) {
        addDetailButton.addEventListener('click', function() {
            const detailContainer = document.getElementById('prescription-details');
            const template = document.getElementById('detail-template');

            if (detailContainer && template) {
                const clone = template.content.cloneNode(true);
                detailContainer.appendChild(clone);

                // 重新初始化处方计算器
                initPrescriptionCalculator();

                // 给新添加的删除按钮添加事件
                const newRow = detailContainer.lastElementChild;
                const deleteButton = newRow.querySelector('.remove-detail');
                if (deleteButton) {
                    deleteButton.addEventListener('click', function() {
                        newRow.remove();
                        updatePrescriptionTotal();
                    });
                }
            }
        });
    }
});

// 检查库存水平
document.addEventListener('DOMContentLoaded', function() {
    checkLowStock();
});