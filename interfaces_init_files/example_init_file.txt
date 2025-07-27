from .add_page_label import AddPageLabel
from .create_attachment import CreateAttachment
from .create_page_template import CreatePageTemplate
from .create_page_version import CreatePageVersion
from .create_page import CreatePage
from .delete_page import DeletePage
from .get_labels_by_name import GetLabelsByName
from .get_page_attachments import GetPageAttachments
from .get_page_children import GetPageChildren
from .get_page_info import GetPageInfo
from .get_page_parent import GetPageParent
from .get_page_versions import GetPageVersions
from .get_space_pages import GetSpacePages
from .get_spaces_by_filters import GetSpacesByFilters
from .get_user_by_email import GetUserByEmail
from .remove_page_label import RemovePageLabel
from .search_page_template_by_name import SearchPageTemplateByName
from .search_pages_per_space import SearchPagesPerSpace
from .update_attachment_info import UpdateAttachmentInfo
from .update_page_template_content import UpdatePageTemplateContent
from .update_page import UpdatePage
from .get_space_templates import GetSpaceTemplates



ALL_TOOLS_INTERFACE_1 = [
    AddPageLabel,
    CreateAttachment,
    CreatePageTemplate,
    CreatePageVersion,
    CreatePage,
    DeletePage,
    GetLabelsByName,
    GetPageAttachments,
    GetPageChildren,
    GetPageInfo,
    GetPageParent,
    GetSpacePages,  
    GetSpacesByFilters,
    GetUserByEmail,
    RemovePageLabel,
    SearchPageTemplateByName,
    SearchPagesPerSpace,
    UpdateAttachmentInfo,
    UpdatePageTemplateContent,
    UpdatePage,
    GetPageVersions,
    GetSpaceTemplates
]
