document.addEventListener('DOMContentLoaded', () => {

    // --- Modal detail buka/tutup ---
    window.openModal = function (id) {
        const modal = document.getElementById(id);
        if (!modal) return;
        modal.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    };
    window.closeModal = function (id) {
        const modal = document.getElementById(id);
        if (!modal) return;
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
    };
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.adm-modal-overlay.is-open').forEach(m => closeModal(m.id));
        }
    });

    // --- Dropdown status kustom (pengganti <select> bawaan browser) ---
    const dropdowns = document.querySelectorAll('[data-dropdown]');

    function closeAllDropdowns(except) {
        dropdowns.forEach(dd => { if (dd !== except) dd.classList.remove('is-open'); });
    }

    dropdowns.forEach(dropdown => {
        const toggleBtn = dropdown.querySelector('[data-dropdown-toggle]');
        const items = dropdown.querySelectorAll('[data-value]');
        const input = dropdown.querySelector('[data-dropdown-input]');
        const form = dropdown.querySelector('[data-dropdown-form]');

        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = dropdown.classList.contains('is-open');
            closeAllDropdowns();
            if (!isOpen) dropdown.classList.add('is-open');
        });

        items.forEach(item => {
            item.addEventListener('click', () => {
                const value = item.getAttribute('data-value');
                if (input.value === value) {
                    dropdown.classList.remove('is-open');
                    return;
                }
                input.value = value;
                form.submit();
            });
        });
    });

    document.addEventListener('click', () => closeAllDropdowns());

});