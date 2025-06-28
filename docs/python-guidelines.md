# Python Coding Guidelines

## **Code Architecture Guidelines**

### **Modularity Rules**
- **File length**: 500 lines as **review trigger** - focus on single responsibility
- **Function length**: Maximum 50 lines per function - ideal 5-20 lines for readability
- **Single responsibility**: Each module and function should have one clear purpose
- **Performance slots**: Use `@dataclass(slots=True)` for memory optimization in Python 3.10+

### **Functional Over Imperative**
- **Use `itertools`**: Leverage `chain()`, `groupby()`, `filter()`, `map()` for data processing
- **Use `functools`**: Apply `reduce()`, `partial()`, `lru_cache()` for function composition
- **Focus on "what" not "how"**: Express intent through function names and composition

```python
# ❌ Avoid - Imperative approach
def process_users(users):
    active_users = []
    for user in users:
        if user.is_active:
            active_users.append(user)
    
    sorted_users = []
    for user in active_users:
        sorted_users.append((user.name.upper(), user.age))
    
    return sorted(sorted_users)

# ✅ Use - Functional approach
from functools import partial
from itertools import filterfalse

def process_users(users):
    return sorted(
        (user.name.upper(), user.age) 
        for user in users 
        if user.is_active
    )
```

### **Core Philosophy**
- **Fewer lines = less maintenance**: Prioritize concise, readable solutions
- **Composition over repetition**: Build complex behavior from simple functions
- **Declarative over procedural**: Express what you want, not step-by-step how

## **Complete AI Agent Ruleset**

### **Mandatory Modern Features (Python 3.13+)**
- Data classes with `@dataclass(slots=True)` for performance
- Built-in generics (`list[str]` not `List[str]`) - required for Python 3.9+
- `functools.cache` instead of `lru_cache(maxsize=None)`
- Type hints on **ALL** functions
- `Self` type for method returns (Python 3.11+)
- `Override` decorator for method overrides (Python 3.12+)

### **Conciseness Rules**
- Walrus operator for assign-and-use patterns - exploit this
- Comprehensions over explicit loops
- Match-case for pattern matching (3+ cases)
- Argument unpacking with `*args`/`**kwargs`

### **Architecture Rules**
- Functional approach using `itertools`/`functools`
- Composition and modularity over monolithic code

**Target**: Minimal, maintainable code that leverages Python's modern capabilities for maximum developer productivity.

## **Modern Development Tools**

### **Unified Tooling**
- **Ruff**: Single tool for linting and formatting (replaces flake8, isort, black)
- **UV**: Fast package manager (replaces pip/poetry for many use cases)
- **pyproject.toml**: Complete project configuration (no setup.py)

### **Performance Patterns**
- **Async concurrency**: `asyncio.TaskGroup` for structured concurrency
- **Memory optimization**: Profile with `tracemalloc` and `memory_profiler`
- **Lazy evaluation**: Generator expressions and `functools.partial`

## **Django-Specific Guidelines (Django 5.2+)**

### **Model Design**
- Use `@dataclass(slots=True)` for non-ORM data structures
- Model managers for reusable query logic
- Business logic in **service functions** (not model methods)
- Model constraints with `Meta.constraints` for data integrity
- Always call `full_clean()` before saving for validation

### **View Architecture**
- Class-based views for CRUD operations
- Service layer for complex business logic
- Mixins for shared functionality
- Focus on single responsibility over line count limits

### **Modern Testing**
- `TestCase.setUpTestData()` instead of fixtures for performance
- `assertNumQueries()` for database query testing
- Service layer unit tests separate from view tests
- `isolate_apps` decorator for model testing

### **Performance Optimization**
- `select_related()` for forward ForeignKey relationships
- `prefetch_related()` for reverse/ManyToMany relationships
- Database-level constraints and indexes
- Query optimization with `django-debug-toolbar`

### **Form & API Patterns**
- ModelForms with proper validation in `clean()` methods
- FormView patterns for complex form handling
- Django REST Framework for API endpoints
- Custom ValidationError with proper error codes
