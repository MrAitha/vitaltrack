// js/components/forms.js

// js/components/forms.js

window.Forms = {
    MealForm: (onSave) => {
        const div = document.createElement('div');
        div.className = 'modal-content';
        div.innerHTML = `
        <div class="modal-header">
            <h3>Log Meal</h3>
            <button class="close-btn">&times;</button>
        </div>
        <form id="meal-form">
            <div class="form-group">
                <label>What did you eat?</label>
                <input type="text" id="meal-name" placeholder="e.g. Avocado Toast" required>
            </div>
            <div class="form-group">
                <label>Ingredients (optional)</label>
                <textarea id="meal-ingredients" placeholder="Comma separated list..."></textarea>
            </div>
            <div class="form-group">
                <label>Time</label>
                <input type="datetime-local" id="meal-time">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Save Meal</button>
        </form>
    `;

        // Set default time to now
        const timeInput = div.querySelector('#meal-time');
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        timeInput.value = now.toISOString().slice(0, 16);

        div.querySelector('form').onsubmit = (e) => {
            e.preventDefault();
            onSave({
                type: 'meal',
                name: div.querySelector('#meal-name').value,
                ingredients: div.querySelector('#meal-ingredients').value,
                timestamp: new Date(div.querySelector('#meal-time').value).toISOString()
            });
        };

        return div;
    },

    SymptomForm: (onSave) => {
        const div = document.createElement('div');
        div.className = 'modal-content';
        div.innerHTML = `
        <div class="modal-header">
            <h3>Log Symptom</h3>
            <button class="close-btn">&times;</button>
        </div>
        <form id="symptom-form">
            <div class="form-group">
                <label>How are you feeling?</label>
                <select id="symptom-type">
                    <option value="energy">Energy Levels</option>
                    <option value="passing_gas">Passing Gas</option>
                    <option value="acidity">Acidity</option>
                    <option value="burping">Burping</option>
                    <option value="pain">Stomach Pain</option>
                    <option value="headache">Headache</option>
                    <option value="mood">Mood</option>
                    <option value="constipation">Constipation</option>
                    <option value="chest_pain_left">Chest Pain (Left)</option>
                    <option value="chest_pain_right">Chest Pain (Right)</option>
                    <option value="chest_pain_middle">Chest Pain (Middle)</option>
                    <option value="rib_pain_left">Rib Pain (Left)</option>
                    <option value="rib_pain_right">Rib Pain (Right)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Severity (1-10)</label>
                <div class="severity-picker">
                    ${[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => `<button type="button" class="severity-btn" data-val="${n}">${n}</button>`).join('')}
                </div>
                <input type="hidden" id="symptom-severity" value="5">
            </div>
            <div class="form-group">
                <label>Time</label>
                <input type="datetime-local" id="symptom-time">
            </div>
            <button type="submit" class="btn btn-secondary btn-block">Save Symptom</button>
        </form>
    `;

        const timeInput = div.querySelector('#symptom-time');
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        timeInput.value = now.toISOString().slice(0, 16);

        const severityBtns = div.querySelectorAll('.severity-btn');
        severityBtns.forEach(btn => {
            btn.onclick = () => {
                severityBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                div.querySelector('#symptom-severity').value = btn.dataset.val;
            };
        });

        div.querySelector('form').onsubmit = (e) => {
            e.preventDefault();
            onSave({
                type: 'symptom',
                symptom: div.querySelector('#symptom-type').value,
                severity: parseInt(div.querySelector('#symptom-severity').value),
                timestamp: new Date(div.querySelector('#symptom-time').value).toISOString()
            });
        };

        return div;
    }
};
