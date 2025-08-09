from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/check-claim', methods=['POST'])
def check_claim():
    data = request.json
    age = int(data.get('age', 0))
    sum_insured = int(data.get('sum_insured', 0))
    hospitalized = data.get('hospitalized', '').strip().lower()
    days = int(data.get('days', 0))
    reason = data.get('reason', '').lower()

    # Arogya Sanjeevani Exclusions (simplified)
    excluded_reasons = ['cosmetic', 'dental', 'fertility', 'plastic', 'hair', 'weight loss']

    # Claim Rules
    if not (18 <= age <= 65):
        return jsonify({'status': 'Rejected ❌', 'message': 'Age not covered (must be 18–65 years)'})
    if not (50000 <= sum_insured <= 500000):
        return jsonify({'status': 'Rejected ❌', 'message': 'Sum Insured must be ₹50,000 – ₹5,00,000'})
    if hospitalized != 'yes':
        return jsonify({'status': 'Rejected ❌', 'message': 'Hospitalization is mandatory for claim'})
    if days < 1:
        return jsonify({'status': 'Rejected ❌', 'message': 'Minimum 1 day hospitalization required'})
    if any(word in reason for word in excluded_reasons):
        return jsonify({'status': 'Rejected ❌', 'message': f'Claim rejected due to exclusion: "{reason}"'})

    return jsonify({'status': 'Approved ✅', 'message': 'Claim is eligible as per Arogya Sanjeevani Policy'})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)

