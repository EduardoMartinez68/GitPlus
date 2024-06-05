// Function to show HTML content in SweetAlert modal
function create_a_new_home_work(title) {
    // HTML content stored in a variable
    const htmlContent = `
        <div class="container">
            <h1 class="title">Add New Task</h1>

            <form id="new-task-form">
                <div class="field">
                    <label class="label">Task Name</label>
                    <div class="control">
                        <input class="input" type="text" id="task-name" placeholder="Enter task name">
                    </div>
                </div>

                <div class="field">
                    <label class="label">Description</label>
                    <div class="control">
                        <textarea class="textarea" id="task-description" placeholder="Enter task description"></textarea>
                    </div>
                </div>

                <div class="field">
                    <label class="label">Due Date</label>
                    <div class="control">
                        <input class="input" type="date" id="task-due-date">
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <button type="submit" class="button is-primary">Add Task</button>
                    </div>
                </div>
            </form>
        </div>
    `;

    Swal.fire({
        title: title,
        html: htmlContent
    });
}