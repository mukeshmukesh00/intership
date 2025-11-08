// Multiple Search Selection Component
class SearchSelection {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            placeholder: options.placeholder || 'Search and select...',
            allowCustom: options.allowCustom || true,
            maxSelections: options.maxSelections || null,
            ...options
        };
        this.selectedItems = new Set();
        this.filteredItems = [];
        this.allItems = options.items || [];
        this.init();
    }

    init() {
        this.createHTML();
        this.bindEvents();
        this.updateDisplay();
    }

    createHTML() {
        this.container.innerHTML = `
            <div class="search-selection-container">
                <div class="search-selection-input-container">
                    <div class="selected-items" id="${this.container.id}-selected"></div>
                    <input type="text" 
                           class="search-selection-input" 
                           id="${this.container.id}-input"
                           placeholder="${this.options.placeholder}"
                           autocomplete="off">
                    <div class="search-selection-dropdown" id="${this.container.id}-dropdown"></div>
                </div>
                <input type="hidden" 
                       name="${this.container.dataset.name || this.container.id}" 
                       id="${this.container.id}-hidden">
            </div>
        `;
    }

    bindEvents() {
        const input = this.container.querySelector('.search-selection-input');
        const dropdown = this.container.querySelector('.search-selection-dropdown');
        const selectedContainer = this.container.querySelector('.selected-items');

        // Input events
        input.addEventListener('input', (e) => this.handleInput(e));
        input.addEventListener('focus', () => this.showDropdown());
        input.addEventListener('blur', (e) => {
            // Delay hiding to allow click events on dropdown
            setTimeout(() => this.hideDropdown(), 150);
        });
        input.addEventListener('keydown', (e) => this.handleKeydown(e));

        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.hideDropdown();
            }
        });

        // Remove item when clicking X
        selectedContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-item')) {
                const item = e.target.dataset.item;
                this.removeItem(item);
            }
        });
    }

    handleInput(e) {
        const query = e.target.value.toLowerCase();
        this.filterItems(query);
        this.showDropdown();
    }

    handleKeydown(e) {
        const dropdown = this.container.querySelector('.search-selection-dropdown');
        const items = dropdown.querySelectorAll('.dropdown-item');
        const activeItem = dropdown.querySelector('.dropdown-item.active');

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.navigateDropdown(items, activeItem, 'down');
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.navigateDropdown(items, activeItem, 'up');
                break;
            case 'Enter':
                e.preventDefault();
                if (activeItem) {
                    this.selectItem(activeItem.dataset.value, activeItem.textContent);
                } else if (e.target.value.trim() && this.options.allowCustom) {
                    this.selectItem(e.target.value.trim(), e.target.value.trim());
                }
                break;
            case 'Escape':
                this.hideDropdown();
                break;
        }
    }

    navigateDropdown(items, activeItem, direction) {
        if (items.length === 0) return;

        // Remove active class from current item
        if (activeItem) {
            activeItem.classList.remove('active');
        }

        let newIndex;
        if (!activeItem) {
            newIndex = direction === 'down' ? 0 : items.length - 1;
        } else {
            const currentIndex = Array.from(items).indexOf(activeItem);
            if (direction === 'down') {
                newIndex = (currentIndex + 1) % items.length;
            } else {
                newIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
            }
        }

        items[newIndex].classList.add('active');
    }

    filterItems(query) {
        if (!query) {
            this.filteredItems = this.allItems.filter(item => !this.selectedItems.has(item));
        } else {
            this.filteredItems = this.allItems.filter(item => 
                !this.selectedItems.has(item) && 
                item.toLowerCase().includes(query)
            );
        }
        this.renderDropdown();
    }

    renderDropdown() {
        const dropdown = this.container.querySelector('.search-selection-dropdown');
        
        if (this.filteredItems.length === 0) {
            dropdown.innerHTML = '<div class="dropdown-item no-results">No results found</div>';
            return;
        }

        dropdown.innerHTML = this.filteredItems.map(item => 
            `<div class="dropdown-item" data-value="${item}">${item}</div>`
        ).join('');

        // Add click events to dropdown items
        dropdown.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', () => {
                this.selectItem(item.dataset.value, item.textContent);
            });
        });
    }

    selectItem(value, displayText) {
        if (this.selectedItems.has(value)) return;
        
        if (this.options.maxSelections && this.selectedItems.size >= this.options.maxSelections) {
            return;
        }

        this.selectedItems.add(value);
        this.updateDisplay();
        this.updateHiddenInput();
        
        // Clear input
        const input = this.container.querySelector('.search-selection-input');
        input.value = '';
        input.focus();
        
        this.hideDropdown();
    }

    removeItem(item) {
        this.selectedItems.delete(item);
        this.updateDisplay();
        this.updateHiddenInput();
    }

    updateDisplay() {
        const selectedContainer = this.container.querySelector('.selected-items');
        const input = this.container.querySelector('.search-selection-input');
        
        if (this.selectedItems.size === 0) {
            selectedContainer.innerHTML = '';
            input.style.display = 'block';
        } else {
            selectedContainer.innerHTML = Array.from(this.selectedItems).map(item => 
                `<span class="selected-item">
                    ${item}
                    <span class="remove-item" data-item="${item}">×</span>
                </span>`
            ).join('');
            input.style.display = 'block';
        }
    }

    updateHiddenInput() {
        const hiddenInput = this.container.querySelector('input[type="hidden"]');
        hiddenInput.value = Array.from(this.selectedItems).join(', ');
    }

    showDropdown() {
        const dropdown = this.container.querySelector('.search-selection-dropdown');
        dropdown.style.display = 'block';
    }

    hideDropdown() {
        const dropdown = this.container.querySelector('.search-selection-dropdown');
        dropdown.style.display = 'none';
        
        // Remove active class from all items
        dropdown.querySelectorAll('.dropdown-item').forEach(item => {
            item.classList.remove('active');
        });
    }

    // Public methods
    getSelectedItems() {
        return Array.from(this.selectedItems);
    }

    setSelectedItems(items) {
        this.selectedItems = new Set(items);
        this.updateDisplay();
        this.updateHiddenInput();
    }

    clear() {
        this.selectedItems.clear();
        this.updateDisplay();
        this.updateHiddenInput();
    }
}

// Initialize search selections when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Skills and Certifications
    const skillsItems = [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'HTML', 'CSS',
        'Flask', 'Django', 'Machine Learning', 'Data Science', 'Web Development',
        'Mobile Development', 'Cloud Computing', 'AWS', 'Azure', 'Git', 'Docker',
        'Kubernetes', 'MongoDB', 'PostgreSQL', 'Redis', 'GraphQL', 'REST API',
        'Agile', 'Scrum', 'DevOps', 'CI/CD', 'Linux', 'Windows', 'macOS',
        'TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Scikit-learn', 'Jupyter',
        'Vue.js', 'Angular', 'TypeScript', 'PHP', 'Ruby', 'Go', 'Rust', 'C++',
        'C#', '.NET', 'Spring Boot', 'Express.js', 'Laravel', 'Rails',
        'Firebase', 'Heroku', 'Netlify', 'Vercel', 'Jenkins', 'Travis CI',
        'Figma', 'Adobe XD', 'Sketch', 'Photoshop', 'Illustrator'
    ];

    // Education levels and fields
    const educationItems = [
        'High School Diploma', 'Associate Degree', 'Bachelor\'s Degree',
        'Master\'s Degree', 'PhD', 'Certificate Program', 'Bootcamp',
        'Computer Science', 'Software Engineering', 'Information Technology',
        'Data Science', 'Cybersecurity', 'Web Development', 'Mobile Development',
        'Business Administration', 'Marketing', 'Finance', 'Accounting',
        'Engineering', 'Mathematics', 'Statistics', 'Physics', 'Chemistry',
        'Biology', 'Psychology', 'Economics', 'International Relations',
        'Graphic Design', 'Digital Marketing', 'Project Management',
        'Human Resources', 'Communications', 'Journalism', 'English Literature'
    ];

    // Languages
    const languageItems = [
        'English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese',
        'Russian', 'Chinese (Mandarin)', 'Chinese (Cantonese)', 'Japanese',
        'Korean', 'Arabic', 'Hindi', 'Bengali', 'Urdu', 'Turkish',
        'Dutch', 'Swedish', 'Norwegian', 'Danish', 'Finnish', 'Polish',
        'Czech', 'Hungarian', 'Romanian', 'Bulgarian', 'Greek', 'Hebrew',
        'Thai', 'Vietnamese', 'Indonesian', 'Malay', 'Tagalog', 'Swahili',
        'Amharic', 'Yoruba', 'Zulu', 'Afrikaans'
    ];

    // Initialize search selections
    if (document.getElementById('skills-selection')) {
        new SearchSelection('skills-selection', {
            items: skillsItems,
            placeholder: 'Search and select skills...',
            allowCustom: true,
            maxSelections: 20
        });
    }

    if (document.getElementById('education-selection')) {
        new SearchSelection('education-selection', {
            items: educationItems,
            placeholder: 'Search and select education...',
            allowCustom: true,
            maxSelections: 10
        });
    }

    if (document.getElementById('languages-selection')) {
        new SearchSelection('languages-selection', {
            items: languageItems,
            placeholder: 'Search and select languages...',
            allowCustom: true,
            maxSelections: 10
        });
    }
});
