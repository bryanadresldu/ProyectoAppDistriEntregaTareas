/**
 * Controlador de la pagina de login (index.html).
 * Al autenticarse, hace una navegacion REAL del navegador (no un simple
 * cambio de visibilidad dentro de la misma pagina) hacia tasks.html o
 * teacher.html, segun el rol del usuario.
 */
document.addEventListener('DOMContentLoaded', () => {
  function homePageFor(role) {
    return role === 'teacher' ? 'teacher.html' : 'tasks.html';
  }

  // Si ya hay una sesion activa (por ejemplo, el usuario volvio a "/"
  // con el back del navegador), lo mandamos directo a su pagina.
  if (Auth.isLoggedIn()) {
    const user = Auth.getUser();
    if (user) {
      window.location.href = homePageFor(user.role);
      return;
    }
  }

  Auth.initLoginForm((user) => {
    window.location.href = homePageFor(user.role);
  });
});
