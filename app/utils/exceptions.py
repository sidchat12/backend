# Custom exceptions for the application

class PortfolioAnalyzerException(Exception):
    """Base exception for the portfolio analyzer"""
    pass

class GitHubServiceException(PortfolioAnalyzerException):
    """Exception for GitHub service errors"""
    pass

class AnalysisException(PortfolioAnalyzerException):
    """Exception for analysis errors"""
    pass

class ResumeParsing_Exception(PortfolioAnalyzerException):
    """Exception for resume parsing errors"""
    pass

class ValidationException(PortfolioAnalyzerException):
    """Exception for validation errors"""
    pass

class ConfigException(PortfolioAnalyzerException):
    """Exception for configuration errors"""
    pass
