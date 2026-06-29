# Переменные
name = "Sergey"
age = 30

# Список (= массив в JS)
skills = ["Vue", "TypeScript", "GSAP"]
skills.append("Python")
print(skills)

# Словарь (= объект в JS)
user = {"name": "Sergey", "role": "fullstack"}
print(user["name"])

# List comprehension (= array.map в JS)
doubled = [x * 2 for x in [1, 2, 3, 4, 5]]
print(doubled)

# Фильтрация (= array.filter в JS)
numbers = [1, 2, 3, 4, 5, 6]
even = [n for n in numbers if n % 2 == 0]
print(even)

# Функция с типами (похоже на TS)
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Sergey"))

# Класс (как class в JS/TS)
class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def describe(self) -> str:
        return f"{self.name} is a {self.role}"

# Наследование
class Developer(User):
    def __init__(self, name: str, skills: list):
        super().__init__(name, "developer")
        self.skills = skills

    def describe(self) -> str:
        base = super().describe()
        return f"{base} | skills: {', '.join(self.skills)}"


sergey = Developer("Sergey", ["Vue", "Python", "FastAPI"])
print(sergey.describe())