# Release 2.0.0 [dev]
- Оптимизирована работа с базой данных
- Добавлена многопоточность (теперь бот работает в нескольких процессах каждый из который выполняет определённую функцию)
- Изменён отчет о статусе сервера
- Исправлен баг связанный с определением времени сообщения в объекте логирования (По итогу в логах было одно и тоже время вечно)
- Исправлен баг с не правильной работай рассылки
- Изменена система хранения временных фото. Теперь они находятся в RAM.
- Изменены типов релизов. Есть 3 типа: stable, unstable, develop, где stable стабильная используется основной базой клиентов git-branch: master; unstable не стабильная версия выпускается для проверкой участниками UVTP разворачивается на отдельном сервере работает от 1 до 7 дней в зависимости от объёма обновления git-branch: develop; develop версия созданная исключительно для разработчиков git-branch: develop.

# Release 1.4.1 [stable]
- Обновлён интерфейс
- Добавлена новая команда /clear_RKM она создана для удаления старого интерфейса
- Обновлена система логирования
- Обновлён генератор кнопок
- Переписана рассылка
- Обновлена система аутентификации
- Исправлено несколько багов
- Повышена читабельность кода

# Release 1.3.2 [beta]
- Added system for checking schedule deletion
- Added the ability to turn off notifications
- Bugs fixed

# Release 1.3.1 [stable]
- Bugs fixed

# Release 1.3.0 [stable] [patch 4]
- Fix issues #27-3
 
# Release 1.3.0 [stable] [patch 3]
- Fix issues #27-2

# Release 1.3.0 [stable] [patch 2]
- Fix issues #27-1
- Bugs fixed

# Release 1.3.0 [stable] [patch 1]
- Added check for D/Z deletion
- Added system for recognizing false messages about D/Z infidelity
- Fix issues #27
- Bugs fixed

# Release 1.3.0 [stable]
- Added a system for notifying administrators in case of incorrect D/Z.
- Added secrets
- Added D/Z and schedule removal system

# Release 1.2.2 [stable]
- Bugs fixed \[call_schedule\]

# Release 1.2.1 [stable]
- The system for calculating time before the start of the lesson has been fixed.
- Bugs fixed

# Release 1.2.0 [stable]
- Added welcome_ani in loging.py
- Bugs fixed
- There was a transition to 'none'

# Release 1.2.0 [beta]
- Added a system for calculating the end of a break or lesson.
- Added checking for emergency situations.
- Automatic update system removed.

# Release 1.1.2 [beta] \[fix v1\]
- Added paragraph button.
- Fixed update system.

# Release 1.1.2 [beta]
- Removed update_date_db command.
- Removed authentication by phone number.
- The status_text function has been renamed to send_status_text.
- The send_message function has been renamed to newsletter.
- The check_admin function has been renamed to check_for_admin.
- Removed unnecessary send_status_text calls.
- A bug related to the updated administration appointment and verification system has been fixed.
- The administration verification system has been redesigned.
- The system for displaying and updating homework has been redesigned from 758 lines of code to 112.
- Fixed a vulnerability that allowed the user to be considered an administrator.
- Logging system has been redesigned.
- The backup system has been redesigned.
- Added a feature to shut down servers.
- Added automatic update feature.