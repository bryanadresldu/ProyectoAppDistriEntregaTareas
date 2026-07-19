/**
 * Logica compartida entre las paginas protegidas (tasks.html, teacher.html):
 * pintar el topbar (nombre, rol, indicador de nodo) y verificar que haya
 * una sesion valida con el rol correcto antes de mostrar la pagina.
 */
const Layout = (() => {
  function paintTopbar(user) {
    document.getElementById('userName').textContent = user.fullName;

    const badge = document.getElementById('roleBadge');
    if (badge) {
      badge.textContent = user.role === 'teacher' ? 'Docente' : 'Estudiante';
      badge.classList.toggle('role-badge--teacher', user.role === 'teacher');
    }

    const indicator = document.getElementById('nodeIndicator');
    if (indicator) {
      document.addEventListener('ad:node', (event) => {
        indicator.textContent = `Nodo: ${event.detail}`;
      });
    }

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        Auth.logout();
        window.location.href = 'index.html';
      });
    }
  }

  function homePageFor(role) {
    return role === 'teacher' ? 'teacher.html' : 'tasks.html';
  }

  /**
   * Debe llamarse al cargar cada pagina protegida, indicando que rol
   * espera esa pagina ('student' o 'teacher'). Si no hay sesion, navega
   * de verdad de vuelta a index.html (login). Si hay sesion pero es del
   * rol equivocado, navega a la pagina que SI le corresponde.
   * Devuelve el usuario si todo esta en orden, o null si redirigio.
   */
  function requireRole(expectedRole) {
    if (!Auth.isLoggedIn()) {
      window.location.href = 'index.html';
      return null;
    }

    const user = Auth.getUser();
    if (!user) {
      Auth.logout();
      window.location.href = 'index.html';
      return null;
    }

    if (user.role !== expectedRole) {
      window.location.href = homePageFor(user.role);
      return null;
    }

    paintTopbar(user);
    return user;
  }

  return { requireRole, homePageFor };
})();
