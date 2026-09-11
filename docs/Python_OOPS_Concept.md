## OOPS

-Object-Oriented Programming is a way of organizing software by grouping together related data (state) and functions (behavior) into objects that represent real-world or logical components of a system.

-Machine learning systems consist of multiple components such as data ingestion, preprocessing, feature engineering, model training, evaluation, and prediction. OOP allows each component to be encapsulated into its own class with clear responsibilities, improving modularity, maintainability, code reuse, and scalability.

When would you use a class versus a function in Python?


I use a function for a self-contained operation where the required inputs can be passed directly and there is no meaningful state that needs to persist between calls. I use a class when a component represents an entity or responsibility that has state and multiple related behaviors operating on that state. For example, in an ML pipeline, I would use a ModelTrainer class because it may maintain the model, configuration, logger, and training state across methods, whereas something like calculate_f1_score() is better implemented as a simple function because it is a stateless calculation.

CLASS
→ Represents a component/entity
→ Has state
→ Has multiple related behaviors
→ Methods operate on that state

FUNCTION
→ Performs a focused operation
→ Inputs → processing → output
→ No meaningful persistent state
→ Easy to reuse independently

## Objects:

- A class is a blueprint.
- An object is an instance of a class.
- One class can create many objects.
- Each object has its own instance state.
- `self` refers to the current object.
- Instance attributes such as `self.model` belong to a particular object.
- Objects contain both state and behavior.
- Pandas DataFrames and scikit-learn models are also Python objects.


The class defines what state and behavior its objects can have. Each object gets its own instance attributes through self, and the methods define the behavior available to that object.

For example:
```python
class Model:

    def __init__(self, name, version):

        self.name = name
        self.version = version

    def show_info(self):

        print(self.name, self.version)
```



# `self` in Python

## 1. What is `self`?

`self` is a reference to the **current object (instance)** on which an instance method is operating.

It allows a method to access the attributes and other methods belonging to that particular object.

> **Important:** `self` is not a property of the class. It is a reference to the current object.

---

## 2. Simple Example

```python
class Student:

    def __init__(self, name, age):

        self.name = name
        self.age = age

    def introduce(self):

        print(
            f"My name is {self.name} "
            f"and I am {self.age} years old."
        )
```


# Constructors and `__init__()` in Python

## 1. What is a constructor?

A constructor is the mechanism used to initialize an object when it is created.

In Python, the method commonly used for this is:

```python
__init__()
```


# State vs Behavior in Python Objects

## 1. What is State?

State is the **data or information currently stored inside an object**.

For example, a `ModelTrainer` object might have:

```text
config
model
metrics
logger n
```

- State is the information currently stored in an object.
- Behavior is what the object can do.
- Instance attributes usually represent state.
- Methods usually represent behavior.
- Behavior can read or modify state.
- State can change during the object's lifecycle.
- Not every temporary value needs to become object state.
- Good classes contain meaningful state and related behavior.
- State and behavior should reflect the responsibility of the class.
- Separation of concerns helps prevent classes from becoming too large.


# Encapsulation

Encapsulation means keeping an object's data and the operations that work on that data together, while controlling how that data is accessed or modified.

## Key Takeaways

- Encapsulation groups data and related behavior together.
- It controls how an object's internal state is accessed or modified.
- Users of a class should interact primarily through its public methods/interface.
- Internal implementation details should not be unnecessarily exposed.
- `_variable` is a convention indicating internal/protected use.
- `__variable` triggers Python name mangling.
- Encapsulation makes code easier to maintain and modify.
- Encapsulation helps centralize validation and business rules.
- Encapsulation allows internal implementation to change without necessarily changing the external interface.
- Not everything needs to be private; access should be designed according to the needs of the system.



# Inheritance

## Key Takeaways

- Inheritance allows a child class to reuse functionality from a parent class.
- The parent is also called a base class.
- The child is also called a subclass or derived class.
- `super()` allows the child to use parent functionality.
- A child can override inherited methods.
- Method overriding allows different subclasses to implement the same interface differently.
- Inheritance is appropriate when there is a meaningful "is-a" relationship.
- Composition represents a "has-a" relationship.
- `ModelTrainer HAS-A model` is composition.
- `RandomForestModel IS-A Model` could be inheritance.
- Inheritance should not be used simply because it is available.
- Prefer simple designs and introduce inheritance when shared behavior genuinely requires it.

# Polymorphism in Python

## 1. What is Polymorphism?

The word polymorphism means:

> "Many forms."

In programming, polymorphism means that **different objects can respond to the same method or interface in their own way**.

For example:

```python
model.train()


Polymorphism means "many forms."
Different objects can respond to the same method/interface differently.
Python supports polymorphism through inheritance and duck typing.
Polymorphism allows code to depend on an interface rather than a specific implementation.
Scikit-learn provides a practical example through common methods such as fit(), predict(), and predict_proba().
Polymorphism reduces the need for large if/elif blocks based on model type.
It makes systems easier to extend with new model types.
Polymorphism and inheritance are related but are not the same concept.
Polymorphism can exist without inheritance.

# Composition in Python

## 1. What is Composition?

Composition means building a class by giving it objects or components that it **uses or owns**.

The simplest way to remember it is:

> **Composition represents a "HAS-A" relationship.**

For example:

```text
Car HAS-A Engine
Computer HAS-A CPU
ModelTrainer HAS-A Model
DataIngestion HAS-A Config
ModelEvaluator HAS-A Model

What is Coupling?

Coupling describes how strongly different components depend on each other.


## Key Takeaways

- Composition represents a "HAS-A" relationship.
- Inheritance represents an "IS-A" relationship.
- `ModelTrainer HAS-A Model`.
- `DataIngestion HAS-A Config`.
- Composition allows components to be replaced without rewriting the class using them.
- Composition often leads to looser coupling.
- Passing dependencies into a class is a form of dependency injection.
- Composition and polymorphism work very well together.
- Composition is often preferable when components have independent responsibilities.
- Inheritance is better suited to genuine parent-child relationships.
- Do not use inheritance simply to avoid writing a few lines of duplicate code.