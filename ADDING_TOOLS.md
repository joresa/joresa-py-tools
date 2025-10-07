# Adding a New Tool - Complete Example

This guide walks you through adding a new tool to the platform using a "Text Analyzer" as an example.

## Step 1: Create the Form (if needed)

Add to `app/tools/forms.py`:

```python
class TextAnalyzerForm(FlaskForm):
    text = TextAreaField('Text to Analyze', validators=[DataRequired()])
    submit = SubmitField('Analyze')
```

## Step 2: Create the Route

Add to `app/tools/routes.py`:

```python
@bp.route('/text-analyzer', methods=['GET', 'POST'])
@login_required
def text_analyzer():
    form = TextAnalyzerForm()
    results = None
    
    if form.validate_on_submit():
        text = form.text.data
        
        # Analyze the text
        results = {
            'characters': len(text),
            'words': len(text.split()),
            'lines': len(text.splitlines()),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()]),
        }
        
        # Record tool usage
        record_tool_usage('text_analyzer')
        
        flash('Text analyzed successfully!', 'success')
    
    return render_template('tools/text_analyzer.html', 
                         title='Text Analyzer',
                         form=form,
                         results=results)
```

## Step 3: Create the Template

Create `app/templates/tools/text_analyzer.html`:

```html
{% extends "base.html" %}

{% block content %}
<div class="row mb-4">
    <div class="col-md-12">
        <h2><i class="bi bi-textarea-t"></i> Text Analyzer</h2>
        <p class="text-muted">Analyze text statistics</p>
    </div>
</div>

<div class="row">
    <div class="col-md-12">
        <div class="card">
            <div class="card-body">
                <form method="POST" novalidate>
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.text.label(class="form-label") }}
                        {{ form.text(class="form-control", rows=10) }}
                        {% if form.text.errors %}
                            <div class="text-danger">
                                {% for error in form.text.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    <div class="d-grid">
                        {{ form.submit(class="btn btn-primary") }}
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

{% if results %}
<div class="row mt-4">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header bg-success text-white">
                <h5><i class="bi bi-bar-chart"></i> Analysis Results</h5>
            </div>
            <div class="card-body">
                <table class="table">
                    <tr>
                        <th>Characters:</th>
                        <td>{{ results.characters }}</td>
                    </tr>
                    <tr>
                        <th>Words:</th>
                        <td>{{ results.words }}</td>
                    </tr>
                    <tr>
                        <th>Lines:</th>
                        <td>{{ results.lines }}</td>
                    </tr>
                    <tr>
                        <th>Paragraphs:</th>
                        <td>{{ results.paragraphs }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}
```

## Step 4: Register the Tool in Database

Option A: Update `init_db.py`:

```python
tools = [
    Tool(
        name='diff_checker',
        display_name='Diff Checker',
        description='Compare two texts or files and see highlighted changes.',
        icon='bi-file-earmark-diff',
        route='/tools/diff',
        is_active=True
    ),
    # Add new tool here
    Tool(
        name='text_analyzer',
        display_name='Text Analyzer',
        description='Analyze text statistics including word count, characters, and more.',
        icon='bi-textarea-t',
        route='/tools/text-analyzer',
        is_active=True
    ),
]
```

Then run:
```bash
python init_db.py
```

Option B: Use Python shell:

```bash
python
>>> from app import create_app, db
>>> from app.models import Tool
>>> app = create_app()
>>> with app.app_context():
...     tool = Tool(
...         name='text_analyzer',
...         display_name='Text Analyzer',
...         description='Analyze text statistics including word count, characters, and more.',
...         icon='bi-textarea-t',
...         route='/tools/text-analyzer',
...         is_active=True
...     )
...     db.session.add(tool)
...     db.session.commit()
```

## Step 5: Add to Navigation (Optional)

If you want to add it to the dropdown menu, edit `app/templates/base.html`:

```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
        Tools
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="{{ url_for('tools.diff_checker') }}">Diff Checker</a></li>
        <li><a class="dropdown-item" href="{{ url_for('tools.text_analyzer') }}">Text Analyzer</a></li>
    </ul>
</li>
```

## Step 6: Test Your Tool

1. Restart the Flask application
2. Navigate to the dashboard
3. You should see "Text Analyzer" card
4. Click to open the tool
5. Test functionality
6. Check analytics to see it's being tracked

## Advanced: Adding Tool-Specific Models

If your tool needs to store data, create a model in `app/models.py`:

```python
class TextAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    word_count = db.Column(db.Integer)
    char_count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TextAnalysis {self.id}>'
```

Then update your route to save data:

```python
analysis = TextAnalysis(
    user_id=current_user.id,
    text=text,
    word_count=results['words'],
    char_count=results['characters']
)
db.session.add(analysis)
db.session.commit()
```

## Bootstrap Icons

Choose from thousands of icons at: https://icons.getbootstrap.com/

Popular choices for tools:
- `bi-gear` - General tool
- `bi-calculator` - Calculator-like tools
- `bi-file-earmark-text` - Text processing
- `bi-graph-up` - Analytics/stats
- `bi-clipboard-check` - Task management
- `bi-calendar-event` - Scheduling
- `bi-diagram-3` - Workflow tools

## Best Practices

1. **Always use `@login_required`** decorator
2. **Call `record_tool_usage()`** for analytics tracking
3. **Use flash messages** for user feedback
4. **Validate input** with WTForms
5. **Handle errors gracefully** with try-except
6. **Keep routes focused** - one tool per route
7. **Use consistent naming** - tool_name in DB, tool-name in URL
8. **Document your tool** in the description field

## Tool Ideas

Here are some ideas for future tools:

1. **URL Shortener** - Create and track short URLs
2. **Password Generator** - Generate secure passwords
3. **Base64 Encoder/Decoder** - Encode/decode Base64
4. **JSON Formatter** - Pretty print and validate JSON
5. **Markdown Preview** - Live markdown editor
6. **Hash Generator** - Generate MD5, SHA256 hashes
7. **QR Code Generator** - Create QR codes from text/URLs
8. **Color Picker** - Color palette and converter
9. **Regex Tester** - Test regular expressions
10. **Unit Converter** - Convert between units

Each of these follows the same pattern outlined above!
