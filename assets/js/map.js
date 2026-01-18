// 地图配置和初始化功能

// ====== 可配置的地图中心点（经纬度）和缩放级别 ======
// 修改这里的数值即可调整地图定位（默认：香港中环附近）
(function() {
    var mapCenterLat = 22.283; // 纬度
    var mapCenterLng = 114.158; // 经度
    var bboxSpan = 0.02; // bbox 半径，用于 iframe 的 viewbox

    function initMapIframe() {
        var iframe = document.getElementById('companyMap');
        if (!iframe) return;
        var left = mapCenterLng - bboxSpan;
        var right = mapCenterLng + bboxSpan;
        var bottom = mapCenterLat - bboxSpan;
        var top = mapCenterLat + bboxSpan;
        var src = 'https://www.openstreetmap.org/export/embed.html?bbox=' + left + '%2C' + bottom + '%2C' + right + '%2C' + top + '&layer=mapnik&marker=' + mapCenterLat + '%2C' + mapCenterLng;
        iframe.src = src;
    }

    // ====== 假期面板（手机风格、支持大陆/香港两个选项卡） ======
    function createHolidaysPanel() {
        /*
          假期数据结构：将每天的特殊状态以 YYYY-MM-DD 为键，值为 'holiday' 或 'work'
          示例可在下方对象中编辑。渲染会以当前月份（当月）并显示 1..30 号。
        */
        var specialDays = {
            mainland: {
                // 示例：2026 年 2 月 17、18 是假，2 月 20 为补班
                '2026-02-17': 'holiday',
                '2026-02-18': 'holiday',
                '2026-02-20': 'work'
            },
            hongkong: {
                '2026-02-17': 'holiday',
                '2026-04-05': 'holiday'
            }
        };

        var panel = document.createElement('aside');
        panel.className = 'side-holidays';
        panel.innerHTML = '\n                    <div class="header">\n                        <div class="title-wrap">\n                            <strong style="font-size:1rem">假期日历</strong>\n                            <div class="tabs">\n                                <button class="tab-btn active" data-tab="mainland">大陆</button>\n                                <button class="tab-btn" data-tab="hongkong">香港</button>\n                            </div>\n                        </div>\n                        <button class="close-btn" aria-label="关闭">&times;</button>\n                    </div>\n                    <div class="content">\n                        <div class="calendar-month">\n                            <div class="month-label"></div>\n                        </div>\n                        <div class="calendar-grid" aria-hidden="false"></div>\n                    </div>';

        document.body.appendChild(panel);

        var content = panel.querySelector('.content');
        var closeBtn = panel.querySelector('.close-btn');
        var tabs = panel.querySelectorAll('.tab-btn');
        var monthLabel = panel.querySelector('.month-label');
        var grid = panel.querySelector('.calendar-grid');

        // 获取要渲染的月份（默认当前月份），并渲染 1..30 号
        var now = new Date();
        var year = now.getFullYear();
        var month = now.getMonth() + 1; // 1-12

        function pad(n){ return n < 10 ? '0' + n : '' + n; }

        function renderCalendar(regionKey) {
            // 更新月份标签（格式 YYYY-MM）
            monthLabel.textContent = year + ' 年 ' + pad(month) + ' 月';

            // 清空 grid
            grid.innerHTML = '';

            for (var d = 1; d <= 30; d++) {
                var dateStr = year + '-' + pad(month) + '-' + pad(d);
                var dayDiv = document.createElement('div');
                dayDiv.className = 'calendar-day';

                var num = document.createElement('div');
                num.className = 'day-number';
                num.textContent = d;
                dayDiv.appendChild(num);

                // 检查是否在 specialDays 中
                var regionMap = specialDays[regionKey] || {};
                if (regionMap[dateStr]) {
                    var badge = document.createElement('div');
                    badge.className = 'day-badge ' + (regionMap[dateStr] === 'holiday' ? 'holiday' : 'work');
                    badge.textContent = regionMap[dateStr] === 'holiday' ? '假' : '班';
                    dayDiv.appendChild(badge);
                }

                grid.appendChild(dayDiv);
            }
        }

        // 初始渲染（大陆）
        renderCalendar('mainland');

        // 选项卡逻辑：切换渲染
        tabs.forEach(function(btn) {
            btn.addEventListener('click', function() {
                tabs.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                var tab = this.getAttribute('data-tab');
                renderCalendar(tab);
            });
        });

        // 关闭按钮
        closeBtn.addEventListener('click', function() { panel.classList.add('closed'); });

        // 如需默认折叠，可启用下一行
        // panel.classList.add('closed');
    }

    // 延迟初始化，确保 DOM 已就绪
    document.addEventListener('DOMContentLoaded', function() {
        initMapIframe();
        // createHolidaysPanel();  // 日历已临时注释
    });
})();