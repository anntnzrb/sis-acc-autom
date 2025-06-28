"""
Utility functions for CarriAcces application.
Security and validation utilities following OWASP best practices.
"""
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from PIL import Image


def validate_image_file(image_file):
    """
    Validate uploaded image file for security and format compliance.
    
    Args:
        image_file: Django UploadedFile instance
        
    Raises:
        ValidationError: If file doesn't meet security requirements
        
    Returns:
        True if validation passes
    """
    if not image_file:
        return True
    
    # Check file size
    max_size = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 5 * 1024 * 1024)
    if image_file.size > max_size:
        raise ValidationError(
            f'El archivo es demasiado grande. Tamaño máximo permitido: {max_size // (1024*1024)}MB'
        )
    
    # Check file extension
    allowed_extensions = getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.webp'])
    file_extension = os.path.splitext(image_file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        allowed_str = ', '.join(allowed_extensions)
        raise ValidationError(
            f'Tipo de archivo no permitido. Tipos permitidos: {allowed_str}'
        )
    
    # Check MIME type
    allowed_types = getattr(settings, 'ALLOWED_IMAGE_TYPES', ['image/jpeg', 'image/png', 'image/webp'])
    if hasattr(image_file, 'content_type') and image_file.content_type not in allowed_types:
        allowed_str = ', '.join(allowed_types)
        raise ValidationError(
            f'Tipo MIME no permitido. Tipos permitidos: {allowed_str}'
        )
    
    # Additional security: Try to open image with PIL to verify it's a valid image
    try:
        # Reset file pointer to beginning
        image_file.seek(0)
        with Image.open(image_file) as img:
            # Verify the image and check for potential security issues
            img.verify()
        # Reset file pointer again for Django to use
        image_file.seek(0)
    except Exception:
        raise ValidationError(
            'El archivo no es una imagen válida o está corrupto.'
        )
    
    return True


def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: Original filename string
        
    Returns:
        Sanitized filename safe for storage
    """
    if not filename:
        return 'unnamed_file'
    
    # Remove path components
    filename = os.path.basename(filename)
    
    # Remove or replace dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '..', '/', '\\']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Ensure filename is not empty after sanitization
    if not filename.strip():
        filename = 'sanitized_file'
    
    return filename


def validate_uploaded_image(image_file):
    """
    Complete image validation workflow.
    
    Args:
        image_file: Django UploadedFile instance
        
    Returns:
        Validated image file
        
    Raises:
        ValidationError: If validation fails
    """
    if not image_file:
        return image_file
    
    # Validate the image file
    validate_image_file(image_file)
    
    # Sanitize the filename
    if hasattr(image_file, 'name'):
        image_file.name = sanitize_filename(image_file.name)
    
    return image_file