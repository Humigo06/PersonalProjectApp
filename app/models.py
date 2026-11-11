from . import db

# class TestEntry(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String(100), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    collections = db.relationship(
        "Collection", back_populates="user",
        cascade="all, delete-orphan"
    )

    projects = db.relationship(
        "Project", back_populates="user",
        cascade="all, delete-orphan"
    )

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"),
        nullable=False
    )

    user = db.relationship("User", back_populates="collections")
    projects = db.relationship("Project",back_populates="collection")

    __table_args__ = (
        db.UniqueConstraint("user_id","name"),
    )

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="idea", nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    user = db.relationship("User", back_populates="projects")
    collection = db.relationship("Collection", back_populates="projects")

    links = db.relationship(
        "ProjectLink", back_populates="project",
        cascade="all, delete-orphan"
    )

    updates = db.relationship(
        "ProgressUpdate", back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProgressUpdate.created_at.desc()"
    )

class ProjectLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    url = db.Column(db.String(2048), nullable=False)

    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False
    )

    project = db.relationship("Project", back_populates="links")

class ProgressUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False
    )

    project = db.relationship("Project", back_populates="updates")