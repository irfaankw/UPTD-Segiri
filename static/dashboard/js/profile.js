document.addEventListener('DOMContentLoaded', function () {

    function bindPhotoPreview(inputId, imgId, emptyId) {
        const input = document.getElementById(inputId);
        const img = document.getElementById(imgId);
        const empty = document.getElementById(emptyId);
        if (!input || !img) return;

        input.addEventListener('change', function () {
            if (!input.files || !input.files[0]) return;
            const reader = new FileReader();
            reader.onload = function (e) {
                img.src = e.target.result;
                img.style.display = 'block';
                if (empty) empty.style.display = 'none';
            };
            reader.readAsDataURL(input.files[0]);
        });
    }

    bindPhotoPreview('id_foto_kepala', 'preview-foto_kepala', 'empty-foto_kepala');
    bindPhotoPreview('id_struktur_organisasi', 'preview-struktur_organisasi', 'empty-struktur_organisasi');

    // Validasi misi kosong di sisi client, biar error-nya inline (konsisten sama field lain), bukan toast
    const misiForm = document.getElementById('misiForm');
    const misiInput = document.getElementById('misiInput');
    const misiError = document.getElementById('misiError');
    if (misiForm && misiInput && misiError) {
        misiForm.addEventListener('submit', function (e) {
            if (!misiInput.value.trim()) {
                e.preventDefault();
                misiError.style.display = 'flex';
                misiInput.focus();
            }
        });
        misiInput.addEventListener('input', function () {
            if (misiInput.value.trim()) misiError.style.display = 'none';
        });
    }

    // Lightbox: klik foto/bagan buat lihat penuh
    const lightbox = document.getElementById('pf-lightbox');
    const lightboxImg = document.getElementById('pf-lightbox-img');

    function openLightbox(img) {
        if (!img || img.style.display === 'none' || !img.src) return;
        lightboxImg.src = img.src;
        lightbox.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }
    function closeLightbox() {
        lightbox.classList.remove('is-open');
        document.body.style.overflow = '';
    }

    document.querySelectorAll('[data-lightbox-trigger]').forEach(function (box) {
        box.addEventListener('click', function () {
            openLightbox(box.querySelector('img'));
        });
    });

    document.getElementById('pfLightboxClose').addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (e) {
        if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeLightbox();
    });

});