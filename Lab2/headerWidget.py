from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLayoutItem,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy
)


class HeaderWidget(QWidget):
    breadcrumb_clicked = pyqtSignal(int)

    def __init__(
        self, username="Invité", role="Utilisateur", parent=None
    ):
        super().__init__(parent)
        self.setObjectName("headerWidget")

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)

        self.breadcrumb_container = QWidget()
        self.breadcrumb_container.setObjectName("breadcrumbContainer")
        self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_container)
        self.breadcrumb_layout.setContentsMargins(0, 0, 0, 0)
        self.breadcrumb_layout.setSpacing(5)

        user_info_layout = QHBoxLayout()

        self.user_label = QLabel(username)
        self.user_label.setObjectName("headerUserLabel")

        self.role_label = QLabel(role)
        self.role_label.setObjectName("headerRoleLabel")

        user_info_layout.addWidget(self.user_label)

        user_info_layout.addStretch()

        user_info_layout.addWidget(self.role_label)

        layout.addLayout(user_info_layout)
        layout.addWidget(self.breadcrumb_container)

        # Initialisation du fil d'Ariane
        self.set_breadcrumbs(["Accueil"])

    def set_user_info(self, username: str, role: str):
        """Met à jour le nom et le rôle de l'utilisateur."""
        self.user_label.setText(username)
        self.role_label.setText(role)

    def set_breadcrumbs(self, items: list[str]):
        """Génère dynamiquement le fil d'Ariane."""
        while self.breadcrumb_layout.count():
            item : QLayoutItem | None = self.breadcrumb_layout.takeAt(0)
            if item is not None and item.widget():
                widget = item.widget()
                if widget is not None: 
                    widget.deleteLater()

        for index, text in enumerate(items):
            is_last = index == len(items) - 1

            if not is_last:
                # Étape cliquable
                btn = QPushButton(text)
                btn.setObjectName("breadcrumbBtn")
                btn.clicked.connect(
                    lambda _, idx=index: self.breadcrumb_clicked.emit(idx)
                )
                self.breadcrumb_layout.addWidget(btn)

                # Séparateur "/"
                sep = QLabel("/")
                sep.setObjectName("breadcrumbSeparator")
                self.breadcrumb_layout.addWidget(sep)
            else:
                # Étape actuelle (non cliquable)
                current_lbl = QLabel(text)
                current_lbl.setObjectName("breadcrumbCurrentLabel")
                self.breadcrumb_layout.addWidget(current_lbl)