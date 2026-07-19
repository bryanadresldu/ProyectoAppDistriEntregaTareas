/**
 * Controlador de tasks.html: tablero de tareas + detalle/entrega.
 * El detalle se abre como una sub-vista DENTRO de esta misma pagina
 * (patron maestro-detalle habitual), pero la pagina en si solo se
 * llega a traves de una navegacion real desde index.html (login) o
 * teacher.html, nunca "desbloqueando" contenido de otra pagina.
 */
const Tasks = (() => {
  let currentTaskId = null;

  function formatDeadline(isoString) {
    // La BD guarda un instante UTC "ingenuo" (sin sufijo de zona horaria).
    // Forzamos su interpretacion como UTC ("Z") antes de convertirlo a la
    // hora local del navegador para mostrarlo.
    const date = new Date(isoString.replace(' ', 'T') + 'Z');
    return date.toLocaleString('es-EC', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }

  function isOverdue(isoString) {
    return new Date() > new Date(isoString.replace(' ', 'T') + 'Z');
  }

  function showGrid() {
    document.getElementById('view-tasks').hidden = false;
    document.getElementById('view-detail').hidden = true;
  }

  function showDetail() {
    document.getElementById('view-tasks').hidden = true;
    document.getElementById('view-detail').hidden = false;
  }

  async function renderTaskGrid() {
    const grid = document.getElementById('taskGrid');
    const messageBox = document.getElementById('tasksMessage');
    grid.innerHTML = '<p>Cargando tareas...</p>';
    Auth.hideMessage(messageBox);

    try {
      const { tasks } = await Api.getTasks();
      grid.innerHTML = '';

      if (tasks.length === 0) {
        grid.innerHTML = '<p>No hay tareas registradas todavia.</p>';
        return;
      }

      tasks.forEach((task) => grid.appendChild(buildTaskCard(task)));
    } catch (err) {
      Auth.showMessage(messageBox, err.message, 'error');
    }
  }

  function buildTaskCard(task) {
    const card = document.createElement('article');
    card.className = 'task-card';

    const overdue = isOverdue(task.deadline);
    const stampClass = overdue ? 'task-card__stamp task-card__stamp--overdue' : 'task-card__stamp';
    const stampText = overdue ? 'Vencida' : 'Vigente';

    card.innerHTML = `
      <span class="${stampClass}">${stampText}</span>
      <p class="task-card__code">${escapeHtml(task.code)}</p>
      <h3 class="task-card__title">${escapeHtml(task.title)}</h3>
      <p class="task-card__deadline">Vence: <strong>${formatDeadline(task.deadline)}</strong></p>
    `;

    card.addEventListener('click', () => openDetail(task.id));
    return card;
  }

  function openDetail(taskId) {
    currentTaskId = taskId;
    showDetail();
    renderTaskDetail(taskId);
  }

  async function renderTaskDetail(taskId) {
    const messageBox = document.getElementById('detailMessage');
    Auth.hideMessage(messageBox);

    document.getElementById('submitBlock').hidden = true;
    document.getElementById('submissionBlock').hidden = true;

    try {
      const { task } = await Api.getTask(taskId);

      document.getElementById('detailCode').textContent = task.code;
      document.getElementById('detailTitle').textContent = task.title;
      document.getElementById('detailDeadline').textContent =
        `Fecha limite: ${formatDeadline(task.deadline)}`;
      document.getElementById('detailDescription').textContent = task.description;

      await renderSubmissionOrForm(taskId, task);
    } catch (err) {
      Auth.showMessage(messageBox, err.message, 'error');
    }
  }

  async function renderSubmissionOrForm(taskId, task) {
    try {
      const { submission } = await Api.getSubmissionForTask(taskId);
      showSubmission(submission);
    } catch (err) {
      // 404 significa que aun no hay entrega -> mostrar formulario
      if (isOverdue(task.deadline)) {
        const messageBox = document.getElementById('detailMessage');
        Auth.showMessage(messageBox, 'El plazo de entrega para esta tarea ha finalizado.', 'error');
      } else {
        document.getElementById('submitBlock').hidden = false;
      }
    }
  }

  function showSubmission(submission) {
    document.getElementById('submissionBlock').hidden = false;
    document.getElementById('submitBlock').hidden = true;
    document.getElementById('submissionDate').textContent =
      `Entregado el ${formatDeadline(submission.submitted_at)}`;
    document.getElementById('submissionAnswer').textContent = submission.answer;
  }

  function initSubmitForm() {
    const form = document.getElementById('submitForm');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const messageBox = document.getElementById('detailMessage');
      Auth.hideMessage(messageBox);

      const answer = document.getElementById('submitAnswer').value;

      try {
        const { submission } = await Api.submitTask(currentTaskId, answer);
        document.getElementById('submitAnswer').value = '';
        showSubmission(submission);
        Auth.showMessage(messageBox, 'Entrega registrada correctamente.', 'success');
      } catch (err) {
        Auth.showMessage(messageBox, err.message, 'error');
      }
    });
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function init() {
    if (!Layout.requireRole('student')) return; // redirige si no corresponde

    document.getElementById('backToTasksBtn').addEventListener('click', showGrid);
    document.getElementById('refreshTasksBtn').addEventListener('click', renderTaskGrid);
    initSubmitForm();

    showGrid();
    renderTaskGrid();
  }

  document.addEventListener('DOMContentLoaded', init);

  return {};
})();
