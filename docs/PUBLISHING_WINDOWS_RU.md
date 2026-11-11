# ContactImpactBench v0.1.4 — Windows: корректировка авторов и релиз

Стабильный репозиторий: https://github.com/spodlesny2318-arch/ContactImpactBench

Работайте в **существующем локальном Git-репозитории**, содержащем pyproject.toml.
Не создавайте `git init` повторно. Распакуйте в корень репозитория архив
`ContactImpactBench_v0.1.4_AUTHOR_PATCH.zip` с заменой файлов. Проверьте:

```powershell
git status --short
git diff -- pyproject.toml CITATION.cff README.md CHANGELOG.md
```

Проверка исходников и полная регрессия (существующая виртуальная среда):

```powershell
.\.venv_cib013\Scripts\python.exe -m pip install -e ".[test]"
.\.venv_cib013\Scripts\python.exe -m pytest -q
.\.venv_cib013\Scripts\python.exe -m contactimpactbench verify --full
```

После проверки:

```powershell
git add .
git commit -m "Correct software authors and citation metadata for v0.1.4"
git push origin main
```

Дождитесь GitHub Actions 4/4 PASS. Только после этого ставьте тег
`v0.1.4` на проверенный коммит и публикуйте новую версию PyPI.

Важно: никогда не переписывайте тег v0.1.3 и не заменяйте релизные файлы
0.1.3. После завершения релиза 0.1.4 загрузите в Zenodo именно архив
Source code (zip) от **v0.1.4**, а не от v0.1.3.

Не вставляйте токен PyPI в терминал как команду и не публикуйте секреты в чат.
