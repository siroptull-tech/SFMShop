# Git Workflow для проекта SFMShop

## Использованные команды Git
- git init - инициализация репозитория
- git add - добавление файлов в staging area
- git commit - сохранение изменений в историю
- git push - отправка изменений на GitHub
- git pull - получение изменений с GitHub
- git checkout -b - создание новой ветки
- git merge - слияние веток
- git rebase - перенос коммитов поверх другой ветки
- git stash - временное сохранение изменений
- git log - просмотр истории коммитов
- git diff - сравнение изменений между ветками
- git reset --soft - отмена коммитов с сохранением кода
- git revert - отмена коммита через новый коммит
- git branch -a - просмотр всех веток включая удалённые
- git show - просмотр конкретного коммита

## Созданные ветки
- main - основная ветка проекта
- feature/add-discount-system - система скидок в классе Product
- feature/add-email-validation - валидация email в классе User
- feature/add-inventory-management - управление складом в Product
- feature/add-shipping - расчёт доставки в Product
- feature/add-logging - система логирования
- feature/add-caching - система кэширования
- feature/add-discount - скидка в get_total_price
- feature/round-price - округление в get_total_price
- feature/test-conflict - тестовый конфликт в get_total_price
- feature/test-rebase - демонстрация rebase

## Разрешённые конфликты

### Конфликт 1 — feature/test-conflict
файл: src/models/product.py, метод get_total_price
одна ветка добавила налог, другая скидку
решение: объединили оба параметра в один метод

### Конфликт 2 — feature/add-shipping
файл: src/models/product.py
одна ветка добавила calculate_shipping, другая get_category в одно место
решение: оставили оба метода

### Конфликт 3 — feature/round-price
файл: src/models/product.py, метод get_total_price
feature/add-discount добавила скидку 0.9
feature/round-price добавила round()
решение: объединили — return round(self.price * self.quantity * 0.9, 2)

## Стратегия работы с ветками
- main всегда стабильный, никто не коммитит напрямую
- каждая задача в отдельной ветке feature/название
- перед созданием PR обновляем ветку из main
- PR проходит ревью, только потом вливается в main
- коммиты с понятными сообщениями что и зачем сделано
- перед слиянием лишние fix-коммиты склеиваются в один через squash
