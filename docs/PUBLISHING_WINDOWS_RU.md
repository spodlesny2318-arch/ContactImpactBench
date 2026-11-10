# ContactImpactBench v0.1.3 — исходники, GitHub и PyPI (Windows)

## 1. GitHub

Репозиторий: https://github.com/spodlesny2318-arch/ContactImpactBench

Для первой загрузки откройте PowerShell **в каталоге с `pyproject.toml`**:

```powershell
 git --version
 git init -b main
 git add .
 git status --short
 git commit -m "Initial public source release v0.1.3"
 git remote add origin https://github.com/spodlesny2318-arch/ContactImpactBench.git
 git push -u origin main
```

Если `git init -b main` не поддерживается, используйте:

```powershell
 git init
 git branch -M main
```

При первом коммите Git может попросить настроить имя и почту автора
(предпочтительно в настройках GitHub иметь приватность email). Не вводите
никаких GitHub паролей или API-токенов в команду. Git Credential Manager
может открыть браузер для авторизации.

**Проверка безопасности:** перед `git add .` убедитесь, что нет файлов `.env`,
`*.pypirc`, приватных паролей, ключей и выгрузок терминала. `dist/`, `.venv*/`
игнорируются. Команда `git status --short` должна показывать только
предназначенные к публикации исходники, документы и эталонные CSV.

## 2. Регрессия из исходников

```powershell
py -m venv .venv_release
.\.venv_release\Scripts\python.exe -m pip install -e ".[test]"
.\.venv_release\Scripts\python.exe -m pip check
.\.venv_release\Scripts\python.exe -m pytest -q
.\.venv_release\Scripts\python.exe -m contactimpactbench verify --full
```

## 3. Сборка и Twine

```powershell
py -m pip install --upgrade build twine
py -m build
py -m twine check .\dist\*
```

На индекс PyPI отправляйте **только** wheel и sdist с номером `0.1.3`.
Не используйте для новой версии архивы `0.1.2`.

## 4. Основной PyPI (после проверок)

После успешной публикации исходников и тестов можно использовать отдельный
API-токен **именно pypi.org**, или настроить GitHub Trusted Publishing.
Никогда не вставляйте токен непосредственно в PowerShell, в чат, GitHub
Issues, коммиты или скриншоты.

```powershell
py -m twine upload .\dist\contactimpactbench-0.1.3-py3-none-any.whl .\dist\contactimpactbench-0.1.3.tar.gz
```

После успешной загрузки в основной PyPI создайте новую venv и проверьте
установку с индекса и регрессию 64/64.

## 5. TestPyPI (история)

Пакет `0.1.2` уже публично опубликован и установлен в чистой Windows-среде:
https://test.pypi.org/project/contactimpactbench/0.1.2/

**Разграничение:** TestPyPI и PyPI — разные индексы. Дистрибутивы уже
опубликованной версии нельзя заменить файлами с тем же именем.
