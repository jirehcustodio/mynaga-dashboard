"""Database models for MyNaga Dashboard."""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between Cases and Offices
case_office_association = Table(
    'case_office_association',
    Base.metadata,
    Column('case_id', Integer, ForeignKey('cases.id')),
    Column('office_id', Integer, ForeignKey('offices.id'))
)

# Association table for Cases and Clusters
case_cluster_association = Table(
    'case_cluster_association',
    Base.metadata,
    Column('case_id', Integer, ForeignKey('cases.id')),
    Column('cluster_id', Integer, ForeignKey('clusters.id'))
)


class Case(Base):
    """Case/Report model."""
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    control_no = Column(String(50), unique=True, index=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    category = Column(String(100))
    sender_location = Column(String(255))
    barangay = Column(String(100))
    description = Column(Text)
    attached_media = Column(String(500))  # URLs to media
    reported_by = Column(String(255))
    contact_number = Column(String(20))
    cluster = Column(String(255))  # Column D in Google Sheets
    link_to_report = Column(String(500))
    office = Column(String(255))  # Column I in Google Sheets  
    mynaga_app_status = Column(String(50))  # Column M in Google Sheets
    updates_sent_to_user = Column(Boolean, default=False)  # Legacy boolean field
    updates_sent_to_user_new = Column(Text)  # Column N - Auto-response message (TEXT)
    office_progress_updates = Column(Text)
    brgy_from_cluster = Column(String(100))
    hours_before_deployed = Column(Integer)
    last_status_update_datetime = Column(DateTime)
    screened_by = Column(String(255))
    status = Column(String(50), default='OPEN')  # OPEN/RESOLVED/FOR REROUTING
    updates_sent = Column(Boolean, default=False)
    case_aging = Column(Integer)  # days
    month = Column(String(20))
    feedback_marked = Column(Boolean, default=False)
    refined_category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    offices = relationship("Office", secondary=case_office_association, back_populates="cases")
    clusters = relationship("Cluster", secondary=case_cluster_association, back_populates="cases")
    updates = relationship("CaseUpdate", back_populates="case", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="case", cascade="all, delete-orphan")


class Office(Base):
    """Office model."""
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    code = Column(String(50))
    location = Column(String(255))
    contact_person = Column(String(255))
    contact_number = Column(String(20))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cases = relationship("Case", secondary=case_office_association, back_populates="offices")


class Cluster(Base):
    """Cluster/Group model for organizing cases."""
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    color = Column(String(10))  # Hex color for UI
    barangay = Column(String(100))
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cases = relationship("Case", secondary=case_cluster_association, back_populates="clusters")


class CaseUpdate(Base):
    """Status updates for cases."""
    __tablename__ = "case_updates"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'), index=True)
    update_text = Column(Text)
    updated_by = Column(String(255))
    update_timestamp = Column(DateTime, default=datetime.utcnow)
    status_after_update = Column(String(50))

    # Relationships
    case = relationship("Case", back_populates="updates")


class Tag(Base):
    """Tags for organizing and categorizing cases."""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'), index=True)
    tag_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    case = relationship("Case", back_populates="tags")
