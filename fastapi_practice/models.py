from sqlalchemy import Column, Integer, String, Numeric

from database import Base


class Wikistats(Base):
    __tablename__ = "wikistats"

    id = Column(Integer, primary_key=True, index=True)
    page_name = Column(String)
    word_ranked_1 = Column(String)
    relative_frequency_1 = Column(Numeric(6, 4))
    word_ranked_2 = Column(String)
    relative_frequency_2 = Column(Numeric(6, 4))
    word_ranked_3 = Column(String)
    relative_frequency_3 = Column(Numeric(6, 4))
    word_ranked_4 = Column(String)
    relative_frequency_4 = Column(Numeric(6, 4))
    word_ranked_5 = Column(String)
    relative_frequency_5 = Column(Numeric(6, 4))
    word_ranked_6 = Column(String)
    relative_frequency_6 = Column(Numeric(6, 4))
    word_ranked_7 = Column(String)
    relative_frequency_7 = Column(Numeric(6, 4))
    word_ranked_8 = Column(String)
    relative_frequency_8 = Column(Numeric(6, 4))
    word_ranked_9 = Column(String)
    relative_frequency_9 = Column(Numeric(6, 4))
    word_ranked_10 = Column(String)
    relative_frequency_10 = Column(Numeric(6, 4))
