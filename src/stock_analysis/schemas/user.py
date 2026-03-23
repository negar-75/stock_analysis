from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, field_validator
from pydantic_core.core_schema import ValidationInfo
import phonenumbers


class UserBaseModel(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PasswordValidationMixin:
    @field_validator("new_password", "password_1", check_fields=False)
    @classmethod
    def password_validation(cls, v: SecretStr):
        value = v.get_secret_value()

        if not value:
            raise ValueError("Password is required")

        if len(value) < 12:
            raise ValueError("Password length must be at least 12 characters")

        return v

class PhoneValidation:
    @field_validator("phone")
    @classmethod
    def phone_validation(cls,v:str):
        try:
            parsed = phonenumbers.parse(v)
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format")
        return v
        



class UserCreate(UserBaseModel, PasswordValidationMixin,PhoneValidation):
    user_name: str
    email: EmailStr
    phone: str
    password_1: SecretStr
    password_2: SecretStr

    @field_validator("password_2")
    @classmethod
    def passwords_match(cls, v: SecretStr, info: ValidationInfo) -> SecretStr:
        if (
            "password_1" in info.data
            and v.get_secret_value() != info.data["password_1"].get_secret_value()
        ):
            raise ValueError("passwords do not match")
        return v


class UserUpdatePassword(BaseModel, PasswordValidationMixin):
    old_password: SecretStr
    new_password: SecretStr


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class UserLoginResponse(BaseModel):
    id: UUID
    access_token: str
    token_type: str = "bearer"


class UserResponse(UserBaseModel):
    id: UUID
