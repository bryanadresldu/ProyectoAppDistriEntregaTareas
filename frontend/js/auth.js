const Auth = (() => {
  function getUser() {
    const raw = sessionStorage.getItem('ad_user');
    return raw ? JSON.parse(raw) : null;
  }

  function setUser(user) {
    sessionStorage.setItem('ad_user', JSON.stringify(user));
  }

  function isLoggedIn() {
    return Boolean(Api.getToken());
  }

  function logout() {
    Api.clearToken();
  }

  function initLoginForm(onSuccess) {
    const form = document.getElementById('loginForm');
    const messageBox = document.getElementById('loginMessage');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      hideMessage(messageBox);

      const email = document.getElementById('loginEmail').value.trim();
      const password = document.getElementById('loginPassword').value;

      try {
        const { token, user } = await Api.login(email, password);
        Api.setToken(token);
        setUser(user);
        onSuccess(user);
      } catch (err) {
        showMessage(messageBox, err.message, 'error');
      }
    });
  }

  function showMessage(box, text, type) {
    box.textContent = text;
    box.className = `alert alert--${type}`;
    box.hidden = false;
  }

  function hideMessage(box) {
    box.hidden = true;
  }

  return { getUser, setUser, isLoggedIn, logout, initLoginForm, showMessage, hideMessage };
})();
