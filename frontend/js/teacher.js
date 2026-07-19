const Teacher = (() => {
  function formatDeadline(isoString) {
    // La base de datos guarda la fecha limite como un instante UTC "ingenuo"
    // (sin sufijo de zona horaria). Le agregamos "Z" para que el navegador
    // lo interprete correctamente como UTC y lo convierta a la hora local
    // del usuario al mostrarlo (en vez de asumir que "21:38" ya es su hora local).
    const date = new Date(isoString.replace(' ', 'T') + 'Z');
    return date.toLocaleString('es-EC', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  async function renderTaskList() {
    const list = document.getElementById('teacherTaskList');
    list.innerHTML = '<p>Cargando tareas...</p>';

    try {
      const { tasks } = await Api.getTasks();
      list.innerHTML = '';

      if (tasks.length === 0) {
        list.innerHTML = '<p>Aun no has registrado ninguna tarea.</p>';
        return;
      }

      tasks.forEach((task) => {
        const card = document.createElement('article');
        card.className = 'task-card task-card--static';
        card.innerHTML = `
          <p class="task-card__code">${escapeHtml(task.code)}</p>
          <h3 class="task-card__title">${escapeHtml(task.title)}</h3>
          <p class="task-card__deadline">Vence: <strong>${formatDeadline(task.deadline)}</strong></p>
        `;
        list.appendChild(card);
      });
    } catch (err) {
      list.innerHTML = `<p>No se pudo cargar el listado de tareas.</p>`;
    }
  }

  function initForm() {
    const form = document.getElementById('teacherTaskForm');
    const messageBox = document.getElementById('teacherMessage');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      Auth.hideMessage(messageBox);

      const localDeadlineValue = document.getElementById('teacherDeadline').value;

      const payload = {
        title: document.getElementById('teacherTitle').value.trim(),
        code: document.getElementById('teacherCode').value.trim(),
        description: document.getElementById('teacherDescription').value.trim(),
        // El input datetime-local devuelve una hora "ingenua" (sin zona
        // horaria), que el navegador interpreta como hora LOCAL del
        // usuario. Convertimos a un instante UTC explicito (con "Z") antes
        // de enviarlo, para que el backend lo interprete igual sin
        // importar en que zona horaria corra el contenedor.
        deadline: localDeadlineValue ? new Date(localDeadlineValue).toISOString() : ''
      };

      try {
        await Api.createTask(payload);
        form.reset();
        Auth.showMessage(messageBox, 'Tarea registrada correctamente.', 'success');
        renderTaskList();
      } catch (err) {
        Auth.showMessage(messageBox, err.message, 'error');
      }
    });
  }

  function init() {
    if (!Layout.requireRole('teacher')) return; // redirige si no corresponde

    initForm();
    renderTaskList();
  }

  document.addEventListener('DOMContentLoaded', init);

  return { renderTaskList, initForm };
})();
