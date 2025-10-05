from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Page(Base):
    __tablename__ = "page"

    id: Mapped[int]
    title: Mapped[str]
    url: Mapped[str]
    # TODO: Categories

    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="page", cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunk"

    id: Mapped[int]
    content: Mapped[str]
    page_id: Mapped[int] = mapped_column(ForeignKey("page.id"))

    page: Mapped["Page"] = relationship(back_populates="chunks")

class User(Base):
    __tablename__ = "user"

    id: Mapped[int]
    name: Mapped[str]
    password_hash: Mapped[str]


class Chat(Base):
    __tablename__ = "chat"

    question: Mapped[str]
    answer: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="chats")
