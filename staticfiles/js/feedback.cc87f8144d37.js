document.addEventListener('DOMContentLoaded', () => {
    // ===== ELEMENTS =====
    const modal = document.getElementById('feedback-modal');
    if (!modal) return;

    const overlay = document.getElementById('feedback-overlay');
    const closeBtn = document.getElementById('feedback-close');
    const staticTriggers = document.querySelectorAll('.feedback-trigger');
    const fab = document.getElementById('feedback-fab');

    const form = document.getElementById('feedback-form');
    const generalError = document.getElementById('feedback-general-error');
    const submitBtn = document.getElementById('feedback-submit');
    const submitSpinner = document.getElementById('feedback-submit-spinner');
    const submitIcon = document.getElementById('feedback-submit-icon');
    const submitText = document.getElementById('feedback-submit-text');

    const fileInput = document.getElementById('id_lampiran');
    const fileLabel = document.getElementById('feedback-file-label');

    const kategoriRadios = document.querySelectorAll('input[name="kategori"]');
    const kategoriLainnyaWrap = document.getElementById('kategori-lainnya-wrap');
    const kategoriLainnyaInput = document.getElementById('id_kategori_lainnya');

    const toastContainer = document.getElementById('toast-container');

    let isSubmitting = false;

    // ===== MODAL OPEN / CLOSE =====
    function openModal() {
        modal.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    function closeModal(force = false) {
        if (isSubmitting && !force) return; // jangan bisa ditutup paksa saat sedang mengirim
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
        clearAllErrors();
    }

    staticTriggers.forEach((btn) => btn.addEventListener('click', openModal));
    if (closeBtn) closeBtn.addEventListener('click', () => closeModal());
    if (overlay) overlay.addEventListener('click', () => closeModal());
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });

    // ===== FAB: expand on hover (desktop) / tap-to-peek (mobile) =====
    if (fab) {
        let fabExpanded = false;
        let fabCollapseTimer;
        let fabTouchTimer;

        function expandFab() {
            clearTimeout(fabCollapseTimer);
            fab.classList.add('is-expanded');
            fabExpanded = true;
        }
        function collapseFab() {
            fab.classList.remove('is-expanded');
            fabExpanded = false;
        }
        function scheduleCollapse() {
            clearTimeout(fabCollapseTimer);
            fabCollapseTimer = setTimeout(collapseFab, 180);
        }

        fab.addEventListener('mouseenter', expandFab);
        fab.addEventListener('mouseleave', scheduleCollapse);

        fab.addEventListener('touchstart', (e) => {
            if (!fabExpanded) {
                e.preventDefault();
                expandFab();
                clearTimeout(fabTouchTimer);
                fabTouchTimer = setTimeout(collapseFab, 2500);
            }
        }, { passive: false });

        fab.addEventListener('click', () => {
            clearTimeout(fabCollapseTimer);
            clearTimeout(fabTouchTimer);
            openModal();
        });
    }

    // ===== Kategori "Lainnya" toggle =====
    kategoriRadios.forEach((radio) => {
        radio.addEventListener('change', () => {
            if (radio.value === 'lainnya' && radio.checked) {
                kategoriLainnyaWrap.classList.remove('hidden');
            } else if (radio.checked) {
                kategoriLainnyaWrap.classList.add('hidden');
                kategoriLainnyaInput.value = '';
                hideError('kategori_lainnya');
            }
        });
    });

    // ===== File label =====
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', () => {
            fileLabel.textContent = fileInput.files.length
                ? fileInput.files[0].name
                : 'Pilih file (foto/dokumen)';
        });
    }

    // ===== Error helpers =====
    function showError(fieldName, message) {
        const el = document.getElementById(`error-${fieldName}`);
        if (el) {
            el.textContent = message;
            el.classList.remove('hidden');
        }
    }
    function hideError(fieldName) {
        const el = document.getElementById(`error-${fieldName}`);
        if (el) el.classList.add('hidden');
    }
    function clearAllErrors() {
        ['kategori', 'kategori_lainnya', 'pesan'].forEach(hideError);
        generalError.classList.add('hidden');
    }

    function validateClientSide() {
        clearAllErrors();
        let valid = true;

        const kategoriChecked = document.querySelector('input[name="kategori"]:checked');
        if (!kategoriChecked) {
            showError('kategori', 'Silakan pilih salah satu kategori.');
            valid = false;
        } else if (kategoriChecked.value === 'lainnya' && !kategoriLainnyaInput.value.trim()) {
            showError('kategori_lainnya', 'Mohon jelaskan kategori yang Anda maksud.');
            valid = false;
        }

        const pesanField = form.querySelector('[name="pesan"]');
        if (!pesanField.value.trim()) {
            showError('pesan', 'Pesan tidak boleh kosong.');
            valid = false;
        }

        return valid;
    }

    // ===== Toast =====
    function showToast(message, isSuccess = true) {
        const el = document.createElement('div');
        el.className = `toast pointer-events-auto flex items-center gap-3 max-w-md w-full md:w-auto rounded-lg border px-4 py-3 shadow-2xl bg-surface-container-high ${
            isSuccess ? 'border-primary-container' : 'border-error'
        }`;

        const iconSvg = isSuccess
            ? '<svg class="w-5 h-5 shrink-0 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
            : '<svg class="w-5 h-5 shrink-0 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>';

        el.innerHTML = `${iconSvg}<span class="text-sm text-on-surface">${message}</span>`;
        toastContainer.appendChild(el);

        requestAnimationFrame(() => el.classList.add('is-visible'));

        setTimeout(() => {
            el.classList.remove('is-visible');
            setTimeout(() => el.remove(), 300);
        }, 4500);
    }

    // ===== Submit =====
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function setSubmittingState(submitting) {
        isSubmitting = submitting;
        submitBtn.disabled = submitting;
        form.classList.toggle('feedback-form-submitting', submitting);
        submitSpinner.classList.toggle('hidden', !submitting);
        submitIcon.classList.toggle('hidden', submitting);
        submitText.textContent = submitting ? 'Mengirim...' : 'Kirim Masukan';
    }

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (isSubmitting) return;

            if (!validateClientSide()) return;

            setSubmittingState(true);
            generalError.classList.add('hidden');

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    body: new FormData(form),
                });
                const data = await response.json();

                if (data.success) {
                    form.reset();
                    if (fileLabel) fileLabel.textContent = 'Pilih file (foto/dokumen)';
                    kategoriLainnyaWrap.classList.add('hidden');

                    // PENTING: lepas dulu status "sedang mengirim" sebelum menutup modal,
                    // supaya guard di closeModal() tidak memblokirnya (ini yang jadi bug sebelumnya).
                    setSubmittingState(false);
                    closeModal(true);
                    showToast(data.message, true);
                    return;
                } else {
                    Object.entries(data.errors).forEach(([field, errs]) => {
                        if (errs && errs[0]) showError(field, errs[0].message);
                    });
                }
            } catch (err) {
                generalError.textContent = 'Terjadi kesalahan jaringan. Silakan coba lagi.';
                generalError.classList.remove('hidden');
            } finally {
                setSubmittingState(false);
            }
        });
    }
});