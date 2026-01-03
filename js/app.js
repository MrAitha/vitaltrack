// js/app.js
// js/app.js

class App {
    constructor() {
        this.store = new window.Store();
        this.currentView = 'dashboard';
        this.modal = document.getElementById('modal-container');
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupActionButtons();
        this.render();

        // Global click handler to close modal
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal || e.target.classList.contains('close-btn')) {
                this.closeModal();
            }
        });

        console.log('💚 VitalTrack Initialized');
    }

    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                navItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');
                this.currentView = item.dataset.view;
                this.render();
            });
        });
    }

    setupActionButtons() {
        document.getElementById('quick-meal-btn').onclick = () => this.openModal('meal');
        document.getElementById('quick-symptom-btn').onclick = () => this.openModal('symptom');
    }

    openModal(type) {
        this.modal.innerHTML = '';
        let form;
        if (type === 'meal') {
            form = window.Forms.MealForm((data) => this.handleSave(data));
        } else {
            form = window.Forms.SymptomForm((data) => this.handleSave(data));
        }
        this.modal.appendChild(form);
        this.modal.classList.remove('hidden');
    }

    closeModal() {
        this.modal.classList.add('hidden');
    }

    handleSave(data) {
        if (data.type === 'meal') {
            this.store.addMeal(data);
        } else {
            this.store.addSymptom(data);
        }
        this.closeModal();
        this.render();
    }

    render() {
        const mainView = document.getElementById('main-view');
        const title = document.getElementById('view-title');

        title.innerText = this.currentView.charAt(0).toUpperCase() + this.currentView.slice(1);

        switch (this.currentView) {
            case 'dashboard':
                this.renderDashboard(mainView);
                break;
            case 'logs':
                this.renderLogs(mainView);
                break;
            case 'symptoms':
                this.renderSymptoms(mainView);
                break;
            case 'trends':
                this.renderTrends(mainView);
                break;
            case 'data':
                this.renderDataManagement(mainView);
                break;
            default:
                mainView.innerHTML = `<div class="empty-state" style="padding: 2rem; border: 1px dashed var(--glass-border); border-radius: 12px; text-align: center; color: var(--text-muted);">
                    Coming soon: ${this.currentView} view
                </div>`;
        }
    }

    renderDashboard(container) {
        const stats = this.store.getStats();
        const recent = this.store.getRecent(5);

        container.innerHTML = `
            <div class="dashboard-grid">
                <div class="card summary-card">
                    <h3>Today's Highlights</h3>
                    <div class="stats">
                        <div class="stat"><span>Meals Logged:</span> <strong>${stats.mealsToday}</strong></div>
                        <div class="stat"><span>Symptoms:</span> <strong>${stats.symptomsToday}</strong></div>
                    </div>
                </div>
                <div class="card recent-logs">
                    <h3>Recent Activity</h3>
                    ${recent.length === 0 ? '<p class="muted">No activity tracked today yet.</p>' : `
                        <ul class="activity-list">
                            ${recent.map(item => `
                                <li class="activity-item">
                                    <span class="icon">${item.type === 'meal' ? '🍱' : '🤒'}</span>
                                    <div class="details">
                                        <strong>${item.name || item.symptom}</strong>
                                        <small>${new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</small>
                                    </div>
                                    ${item.severity ? `<span class="severity-badge sev-${item.severity}">${item.severity}</span>` : ''}
                                </li>
                            `).join('')}
                        </ul>
                    `}
                </div>
            </div>
        `;
    }

    renderLogs(container) {
        const meals = this.store.data.meals.slice().reverse();
        container.innerHTML = `
            <div class="logs-view">
                ${meals.length === 0 ? '<p class="muted">No meals logged yet.</p>' : `
                    <div class="activity-list">
                        ${meals.map(meal => `
                            <div class="card" style="margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem;">
                                <span style="font-size: 1.5rem;">🍱</span>
                                <div>
                                    <strong>${meal.name}</strong>
                                    <p class="muted" style="font-size: 0.85rem;">${meal.ingredients || 'No ingredients listed'}</p>
                                    <small>${new Date(meal.timestamp).toLocaleString()}</small>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `}
            </div>
        `;
    }

    renderSymptoms(container) {
        const symptoms = this.store.data.symptoms.slice().reverse();
        container.innerHTML = `
            <div class="logs-view">
                ${symptoms.length === 0 ? '<p class="muted">No symptoms logged yet.</p>' : `
                    <div class="activity-list">
                        ${symptoms.map(s => `
                            <div class="card" style="margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 1rem;">
                                    <span style="font-size: 1.5rem;">🤒</span>
                                    <div>
                                        <strong style="text-transform: capitalize;">${s.symptom}</strong><br>
                                        <small>${new Date(s.timestamp).toLocaleString()}</small>
                                    </div>
                                </div>
                                <span class="severity-badge sev-${s.severity}">${s.severity}</span>
                            </div>
                        `).join('')}
                    </div>
                `}
            </div>
        `;
    }

    renderTrends(container) {
        const trendData = this.store.getTrendsData(7);
        const uniqueSymptoms = [...new Set(this.store.data.symptoms.map(s => s.symptom))];

        container.innerHTML = `
            <div class="card trends-card" style="margin-bottom: 2rem;">
                <h3>Symptom Frequency (Last 7 Days)</h3>
                <div class="chart-wrapper" style="position: relative; height: 350px; width: 100%; margin-top: 1rem;">
                    <canvas id="symptomChart"></canvas>
                </div>
            </div>

            <div class="card analyzer-card">
                <h3>🔍 Root Cause Analyzer</h3>
                <p class="muted" style="font-size: 0.9rem; margin-bottom: 1.5rem;">Select a symptom to find potential dietary triggers from the 1-12 hours prior to each occurrence.</p>
                
                <div class="analyzer-controls" style="margin-bottom: 2rem;">
                    <select id="symptom-analyzer-select" class="form-control" style="width: auto; min-width: 200px;">
                        <option value="">Select a symptom...</option>
                        ${uniqueSymptoms.map(s => `<option value="${s}">${s.charAt(0).toUpperCase() + s.slice(1)}</option>`).join('')}
                    </select>
                </div>

                <div id="analyzer-results">
                    <div class="empty-state" style="padding: 2rem; border: 1px dashed var(--glass-border); border-radius: 12px; text-align: center; color: var(--text-muted);">
                        Select a symptom to begin analysis
                    </div>
                </div>
            </div>
        `;

        const select = document.getElementById('symptom-analyzer-select');
        select.addEventListener('change', (e) => this.handleSymptomAnalysis(e.target.value));

        const ctx = document.getElementById('symptomChart').getContext('2d');

        if (this.chart) {
            this.chart.destroy();
        }

        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: trendData.labels,
                datasets: trendData.datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#e2e8f0',
                            font: {
                                family: "'Inter', sans-serif"
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#e2e8f0',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#94a3b8'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        }
                    }
                }
            }
        });
    }

    handleSymptomAnalysis(symptomName) {
        const resultsContainer = document.getElementById('analyzer-results');
        if (!symptomName) {
            resultsContainer.innerHTML = `<div class="empty-state" style="padding: 2rem; border: 1px dashed var(--glass-border); border-radius: 12px; text-align: center; color: var(--text-muted);">Select a symptom to begin analysis</div>`;
            return;
        }

        const correlations = this.store.getCorrelations(symptomName);

        if (correlations.length === 0) {
            resultsContainer.innerHTML = `<p class="muted">No strong dietary correlations found for "${symptomName}". Try logging more data!</p>`;
            return;
        }

        resultsContainer.innerHTML = `
            <div class="correlation-list">
                <h4 style="margin-bottom: 1rem;">Potential Triggers for <span style="color: var(--primary-color)">${symptomName}</span>:</h4>
                ${correlations.map(c => `
                    <div class="correlation-item" style="margin-bottom: 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 8px; border: 1px solid var(--glass-border);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <strong>${c.name}</strong>
                            <span class="severity-badge" style="background: ${c.percentage > 50 ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)'}; color: ${c.percentage > 50 ? '#f87171' : '#fbbf24'}; border-color: ${c.percentage > 50 ? 'rgba(239, 68, 68, 0.3)' : 'rgba(245, 158, 11, 0.3)'}">
                                ${c.percentage}% correlation
                            </span>
                        </div>
                        <div class="progress-bar" style="height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden;">
                            <div style="height: 100%; width: ${c.percentage}%; background: ${c.percentage > 50 ? 'var(--primary-color)' : 'var(--secondary-color)'}; transition: width 0.6s ease;"></div>
                        </div>
                        <p class="muted" style="font-size: 0.8rem; margin-top: 0.5rem;">Appeared in ${c.count} out of ${this.store.data.symptoms.filter(s => s.symptom === symptomName).length} instances.</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderDataManagement(container) {
        container.innerHTML = `
            <div class="card data-card">
                <h3>Data Management</h3>
                <p class="muted" style="margin-bottom: 2rem;">Your data is stored locally in your browser. Use the buttons below to export or manage your data.</p>
                
                <div class="data-actions" style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <button id="export-btn" class="btn btn-primary">
                        <span style="margin-right: 0.5rem;">📥</span> Export as JSON
                    </button>
                </div>

                <div style="margin-top: 3rem; padding: 1.5rem; background: rgba(239, 68, 68, 0.05); border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);">
                    <h4 style="color: #f87171; margin-bottom: 0.5rem;">Danger Zone</h4>
                    <p class="muted" style="font-size: 0.85rem; margin-bottom: 1rem;">Clearing your data will permanently remove all logs from this browser.</p>
                    <button id="clear-data-btn" class="btn" style="background: transparent; border: 1px solid #ef4444; color: #ef4444;">Clear All Data</button>
                </div>
            </div>
        `;

        document.getElementById('export-btn').onclick = () => this.store.exportData();
        document.getElementById('clear-data-btn').onclick = () => {
            if (confirm('Are you sure you want to clear ALL data? This cannot be undone.')) {
                localStorage.removeItem(this.store.storageKey);
                location.reload();
            }
        };
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Register Service Worker for PWA support
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('./sw.js')
                .then(reg => console.log('SW Registered', reg))
                .catch(err => console.error('SW Registration failed', err));
        });
    }

    window.app = new App();
});
