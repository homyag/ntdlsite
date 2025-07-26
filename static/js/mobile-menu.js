/**
 * Компактное мобильное меню категорий
 */

class MobileCategoryMenu {
    constructor() {
        this.toggle = document.getElementById('mobileCategoryToggle');
        this.dropdown = document.getElementById('mobileCategoryDropdown');
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        if (!this.toggle || !this.dropdown) {
            console.warn('Mobile category menu elements not found');
            return;
        }
        
        this.bindEvents();
    }
    
    bindEvents() {
        // Открытие/закрытие меню
        this.toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMenu();
        });
        
        // Закрытие по клику вне меню
        document.addEventListener('click', (e) => {
            if (this.isOpen && !this.toggle.contains(e.target) && !this.dropdown.contains(e.target)) {
                this.closeMenu();
            }
        });
        
        // Закрытие по Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeMenu();
            }
        });
        
        // Закрытие после выбора категории
        this.dropdown.addEventListener('click', (e) => {
            if (e.target.tagName === 'A') {
                this.closeMenu();
            }
        });
    }
    
    toggleMenu() {
        if (this.isOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }
    
    openMenu() {
        this.isOpen = true;
        this.toggle.classList.add('active');
        this.dropdown.classList.add('show');
        
        // Аналитика
        this.trackEvent('mobile_category_menu_opened');
    }
    
    closeMenu() {
        this.isOpen = false;
        this.toggle.classList.remove('active');
        this.dropdown.classList.remove('show');
        
        // Аналитика
        this.trackEvent('mobile_category_menu_closed');
    }
    
    trackEvent(eventName) {
        // Интеграция с аналитикой
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                event_category: 'mobile_category_menu'
            });
        }
        
        if (typeof ym !== 'undefined') {
            ym(98660706, 'reachGoal', eventName);
        }
    }
}

// Утилиты
class MobileCategoryMenuUtils {
    static isMobile() {
        return window.innerWidth <= 992;
    }
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    if (MobileCategoryMenuUtils.isMobile()) {
        window.mobileCategoryMenu = new MobileCategoryMenu();
    }
});

// Переинициализация при изменении размера окна
window.addEventListener('resize', () => {
    if (MobileCategoryMenuUtils.isMobile() && !window.mobileCategoryMenu) {
        window.mobileCategoryMenu = new MobileCategoryMenu();
    } else if (!MobileCategoryMenuUtils.isMobile() && window.mobileCategoryMenu) {
        window.mobileCategoryMenu.closeMenu();
    }
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MobileCategoryMenu, MobileCategoryMenuUtils };
}