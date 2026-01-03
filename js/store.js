// js/store.js

window.Store = class Store {
    constructor() {
        this.storageKey = 'vitaltrack_data';
        this.data = this.load();
    }

    load() {
        const saved = localStorage.getItem(this.storageKey);
        return saved ? JSON.parse(saved) : {
            meals: [],
            symptoms: [],
            settings: {
                theme: 'light'
            }
        };
    }

    save() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.data));
    }

    addMeal(meal) {
        this.data.meals.push({
            id: Date.now(),
            timestamp: new Date().toISOString(),
            ...meal
        });
        this.save();
    }

    addSymptom(symptom) {
        this.data.symptoms.push({
            id: Date.now(),
            timestamp: new Date().toISOString(),
            ...symptom
        });
        this.save();
    }

    getStats() {
        const today = new Date().toLocaleDateString();
        const mealsToday = this.data.meals.filter(m => new Date(m.timestamp).toLocaleDateString() === today).length;
        const symptomsToday = this.data.symptoms.filter(s => new Date(s.timestamp).toLocaleDateString() === today).length;
        return { mealsToday, symptomsToday };
    }

    getRecent(limit = 5) {
        const all = [
            ...this.data.meals.map(m => ({ ...m, type: 'meal' })),
            ...this.data.symptoms.map(s => ({ ...s, type: 'symptom' }))
        ];
        return all.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, limit);
    }

    getTrendsData(days = 7) {
        const labels = [];
        const datasets = {}; // { symptomName: [countPerDay] }
        const now = new Date();

        // Initialize last X days
        for (let i = days - 1; i >= 0; i--) {
            const d = new Date(now);
            d.setDate(d.getDate() - i);
            labels.push(d.toLocaleDateString([], { month: 'short', day: 'numeric' }));
        }

        // Get all unique symptoms
        const uniqueSymptoms = [...new Set(this.data.symptoms.map(s => s.symptom))];

        uniqueSymptoms.forEach(sName => {
            datasets[sName] = new Array(days).fill(0);
        });

        // Populate counts
        this.data.symptoms.forEach(s => {
            const sDate = new Date(s.timestamp);
            const diffTime = Math.abs(now - sDate);
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays < days) {
                const index = (days - 1) - diffDays;
                if (datasets[s.symptom]) {
                    datasets[s.symptom][index]++;
                }
            }
        });

        return {
            labels,
            datasets: Object.keys(datasets).map(name => ({
                label: name.charAt(0).toUpperCase() + name.slice(1),
                data: datasets[name],
                backgroundColor: this.getColorForSymptom(name)
            }))
        };
    }

    getColorForSymptom(name) {
        const colors = {
            'passing_gas': 'rgba(255, 99, 132, 0.6)',
            'acidity': 'rgba(255, 159, 64, 0.6)',
            'burping': 'rgba(255, 206, 86, 0.6)',
            'headache': 'rgba(54, 162, 235, 0.6)',
            'nausea': 'rgba(255, 206, 86, 0.6)',
            'fatigue': 'rgba(75, 192, 192, 0.6)',
            'cramps': 'rgba(153, 102, 255, 0.6)',
            'constipation': 'rgba(255, 159, 64, 0.6)',
            'chest_pain_left': 'rgba(255, 0, 0, 0.6)',
            'chest_pain_right': 'rgba(255, 0, 0, 0.6)',
            'chest_pain_middle': 'rgba(255, 0, 0, 0.6)',
            'rib_pain_left': 'rgba(220, 20, 60, 0.6)',
            'rib_pain_right': 'rgba(220, 20, 60, 0.6)'
        };
        return colors[name] || 'rgba(201, 203, 207, 0.6)';
    }

    exportData() {
        try {
            const dataStr = JSON.stringify(this.data, null, 2);
            const blob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `vitaltrack_export_${new Date().toISOString().split('T')[0]}.json`;

            document.body.appendChild(a);
            a.click();

            // Clean up
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 100);
        } catch (error) {
            console.error('Export failed:', error);
            alert('Failed to export data. Please check console for details.');
        }
    }

    getCorrelations(symptomName) {
        if (!symptomName) return [];

        const occurrences = this.data.symptoms.filter(s => s.symptom === symptomName);
        if (occurrences.length === 0) return [];

        const correlations = {}; // { triggerName: count }

        occurrences.forEach(symptom => {
            const symptomTime = new Date(symptom.timestamp);
            const triggersInWindow = new Set(); // Track unique triggers for THIS symptom occurrence

            // Look for meals 2-24 hours prior
            this.data.meals.forEach(meal => {
                const mealTime = new Date(meal.timestamp);
                const diffHours = (symptomTime - mealTime) / (1000 * 60 * 60);

                if (diffHours >= 1 && diffHours <= 12) {
                    // Collect the meal name
                    triggersInWindow.add(meal.name);

                    // Collect individual ingredients
                    if (meal.ingredients) {
                        const ingredients = meal.ingredients.split(',')
                            .map(i => i.trim())
                            .filter(i => i.length > 0);

                        ingredients.forEach(ingredient => {
                            triggersInWindow.add(`Ingredient: ${ingredient}`);
                        });
                    }
                }
            });

            // Increment the global count for each unique trigger found in this window
            triggersInWindow.forEach(trigger => {
                correlations[trigger] = (correlations[trigger] || 0) + 1;
            });
        });

        // Convert to sorted array of correlations
        return Object.entries(correlations)
            .map(([name, count]) => ({
                name,
                count,
                percentage: Math.round((count / occurrences.length) * 100)
            }))
            .sort((a, b) => b.count - a.count);
    }

    importData(data) {
        try {
            if (!data.meals || !data.symptoms) {
                throw new Error('Invalid data format: missing meals or symptoms arrays.');
            }

            this.data = {
                meals: data.meals,
                symptoms: data.symptoms,
                settings: data.settings || { theme: 'light' }
            };

            this.save();
            return true;
        } catch (error) {
            console.error('Import failed:', error);
            return false;
        }
    }
}
