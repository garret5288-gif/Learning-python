// Dark mode toggle with localStorage persistence and CSP-safe external script
(function () {
    try {
        var saved = localStorage.getItem('theme');
        if (saved === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else if (saved === 'light') {
            document.documentElement.removeAttribute('data-theme');
        }
        var btn = document.getElementById('themeToggle');
        if (btn) {
            function setLabel() {
                var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
                btn.textContent = isDark ? 'Light mode' : 'Dark mode';
            }
            setLabel();
            btn.addEventListener('click', function () {
                var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
                var next = isDark ? 'light' : 'dark';
                if (next === 'dark') {
                    document.documentElement.setAttribute('data-theme', 'dark');
                } else {
                    document.documentElement.removeAttribute('data-theme');
                }
                localStorage.setItem('theme', next);
                setLabel();
            });
        }
    } catch (e) {
        // fail silently
    }
})();
