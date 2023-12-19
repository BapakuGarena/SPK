from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class tbl_mobil(Base):
    __tablename__ = 'tbl_mobil'
    nama_mobil: Mapped[str] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column()
    harga: Mapped[int] = mapped_column()
    rate: Mapped[int] = mapped_column()
    ukuran: Mapped[int] = mapped_column()
    
    def __repr__(self) -> str:
        return f"tbl_mobil(nama_mobil={self.nama_mobil!r}, id={self.id!r})"