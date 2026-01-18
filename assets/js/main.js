// 主JavaScript文件 - 包含轮播图、导航、滚动等功能

document.addEventListener('DOMContentLoaded', () => {
    // 轮播图功能
    const carouselSlides = document.querySelectorAll('.carousel-slide');
    const carouselIndicators = document.querySelectorAll('.carousel-indicator');
    const prevButton = document.getElementById('carouselPrev');
    const nextButton = document.getElementById('carouselNext');
    const autoplayButton = document.getElementById('carouselAutoplay');
    let currentSlide = 0;
    let autoplayInterval;
    let autoplayActive = true;
    
    // 初始化轮播图
    function initCarousel() {
        // 设置自动播放
        startAutoplay();
        
        // 为指示器添加点击事件
        carouselIndicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                goToSlide(index);
                resetAutoplay();
            });
        });
        
        // 上一张按钮
        prevButton.addEventListener('click', () => {
            prevSlide();
            resetAutoplay();
        });
        
        // 下一张按钮
        nextButton.addEventListener('click', () => {
            nextSlide();
            resetAutoplay();
        });
        
        // 自动播放按钮
        autoplayButton.addEventListener('click', toggleAutoplay);
        
        // 触摸滑动支持
        let touchStartX = 0;
        let touchEndX = 0;
        
        const carousel = document.querySelector('.carousel');
        carousel.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        carousel.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });
        
        function handleSwipe() {
            const swipeThreshold = 50; // 最小滑动距离
            
            if (touchEndX < touchStartX - swipeThreshold) {
                // 向左滑动，下一张
                nextSlide();
                resetAutoplay();
            } else if (touchEndX > touchStartX + swipeThreshold) {
                // 向右滑动，上一张
                prevSlide();
                resetAutoplay();
            }
        }
    }
    
    // 转到指定幻灯片
    function goToSlide(index) {
        // 隐藏当前幻灯片
        carouselSlides[currentSlide].classList.remove('active');
        carouselIndicators[currentSlide].classList.remove('active');
        
        // 更新当前索引
        currentSlide = index;
        
        // 显示新幻灯片
        carouselSlides[currentSlide].classList.add('active');
        carouselIndicators[currentSlide].classList.add('active');
    }
    
    // 下一张幻灯片
    function nextSlide() {
        let nextIndex = currentSlide + 1;
        if (nextIndex >= carouselSlides.length) {
            nextIndex = 0;
        }
        goToSlide(nextIndex);
    }
    
    // 上一张幻灯片
    function prevSlide() {
        let prevIndex = currentSlide - 1;
        if (prevIndex < 0) {
            prevIndex = carouselSlides.length - 1;
        }
        goToSlide(prevIndex);
    }
    
    // 开始自动播放
    function startAutoplay() {
        if (autoplayActive) {
            autoplayInterval = setInterval(nextSlide, 5000); // 5秒切换一次
            autoplayButton.innerHTML = '<i class="fas fa-pause"></i>';
        }
    }
    
    // 停止自动播放
    function stopAutoplay() {
        clearInterval(autoplayInterval);
        autoplayButton.innerHTML = '<i class="fas fa-play"></i>';
    }
    
    // 切换自动播放状态
    function toggleAutoplay() {
        autoplayActive = !autoplayActive;
        if (autoplayActive) {
            startAutoplay();
        } else {
            stopAutoplay();
        }
    }
    
    // 重置自动播放计时器
    function resetAutoplay() {
        if (autoplayActive) {
            clearInterval(autoplayInterval);
            startAutoplay();
        }
    }
    
    // 初始化轮播图
    initCarousel();
    
    // 移动端菜单切换
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');
    
    mobileToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        mobileToggle.innerHTML = navMenu.classList.contains('active') 
            ? '<i class="fas fa-times"></i>' 
            : '<i class="fas fa-bars"></i>';
    });
    
    // 关闭移动菜单当点击链接时
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            mobileToggle.innerHTML = '<i class="fas fa-bars"></i>';
        });
    });
    
    // 滚动时改变导航栏样式
    window.addEventListener('scroll', () => {
        const header = document.getElementById('header');
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // 返回顶部按钮显示/隐藏
        const backToTop = document.getElementById('backToTop');
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
        
        // 服务卡片动画
        const serviceCards = document.querySelectorAll('.service-card');
        serviceCards.forEach(card => {
            const cardTop = card.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            if (cardTop < windowHeight - 100) {
                card.classList.add('visible');
            }
        });
        
        // 导航链接高亮
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                document.querySelectorAll('.nav-menu a').forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
    
    // 二维码预览功能
    (function(){
        function openImgModal(src, alt){
            var modal = document.getElementById('imgModal');
            var img = document.getElementById('imgModalImg');
            var cap = document.getElementById('imgModalCaption');
            img.src = src;
            img.alt = alt || '二维码';
            cap.textContent = alt || '';
            modal.classList.add('open');
            modal.setAttribute('aria-hidden','false');
        }
        function closeImgModal(){
            var modal = document.getElementById('imgModal');
            var img = document.getElementById('imgModalImg');
            modal.classList.remove('open');
            modal.setAttribute('aria-hidden','true');
            setTimeout(function(){ img.src = ''; }, 200);
        }

        // 小型锚点式 popover（桌面）
        var currentPopover = null;
        function openQrPopover(anchor, src, alt){
            closeQrPopover();
            // 在小屏幕下使用模态替代
            if (window.innerWidth <= 480) { openImgModal(src, alt); return; }

            var img = document.createElement('img');
            img.src = src;
            img.alt = alt || '';
            img.style.maxWidth = '220px';
            img.style.height = 'auto';
            img.style.display = 'block';
            img.loading = 'lazy';

            var pop = document.createElement('div');
            pop.className = 'qr-popover';
            pop.style.position = 'absolute';
            pop.style.zIndex = 3500;
            pop.style.background = 'white';
            pop.style.padding = '8px';
            pop.style.borderRadius = '8px';
            pop.style.boxShadow = '0 8px 20px rgba(0,0,0,0.18)';
            pop.style.transition = 'opacity 180ms ease, transform 180ms ease';
            pop.style.opacity = '0';
            pop.style.transform = 'translateY(6px)';

            pop.appendChild(img);

            document.body.appendChild(pop);
            currentPopover = pop;

            // 计算位置（放在锚点上方优先，如果不足则放下方）
            var rect = anchor.getBoundingClientRect();
            var popRect = { width: 240, height: 260 };
            var left = rect.left + window.pageXOffset + (rect.width/2) - (popRect.width/2);
            left = Math.max(8, Math.min(left, window.pageXOffset + document.documentElement.clientWidth - popRect.width - 8));
            var top = rect.top + window.pageYOffset - popRect.height - 10;
            if (top < window.pageYOffset + 8) {
                top = rect.bottom + window.pageYOffset + 10; // 放下方
            }

            pop.style.left = left + 'px';
            pop.style.top = top + 'px';

            // 触发动画
            requestAnimationFrame(function(){ pop.style.opacity = '1'; pop.style.transform = 'translateY(0)'; });
        }
        function closeQrPopover(){
            if (!currentPopover) return;
            var p = currentPopover;
            p.style.opacity = '0';
            p.style.transform = 'translateY(6px)';
            setTimeout(function(){ if (p.parentNode) p.parentNode.removeChild(p); }, 200);
            currentPopover = null;
        }

        // 点击处理：qr-link 点击显示 popover（桌面）或模态（移动端）
        document.addEventListener('click', function(e){
            var a = e.target.closest('.qr-link');
            if (a && a.dataset && a.dataset.img) {
                e.preventDefault();
                var src = a.dataset.img;
                var title = a.title || (a.querySelector('img') && a.querySelector('img').alt) || '';
                openQrPopover(a, src, title);
                return;
            }

            // 点击遮罩或模态的关闭按钮
            if (e.target.matches('.img-modal-backdrop') || e.target.matches('.img-modal-close')) {
                closeImgModal();
            }

            // 点击非 popover 区域时关闭 popover
            if (currentPopover && !e.target.closest('.qr-popover') && !e.target.closest('.qr-link')) {
                closeQrPopover();
            }
        });

        // Esc 键关闭任一预览
        document.addEventListener('keydown', function(e){
            if (e.key === 'Escape') { closeImgModal(); closeQrPopover(); }
        });
    })();
    
    // 触发滚动事件以初始化
    setTimeout(() => {
        window.dispatchEvent(new Event('scroll'));
    }, 300);
});