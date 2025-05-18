from fastmcp import FastMCP, Context
from wxautox import WeChat
from typing import List, Optional, Union, Dict

# Initialize FastMCP server
mcp = FastMCP(
    name="WeChat Bot Server",
    instructions="""
    This server provides tools for sending WeChat messages.
    Use send_text() to send text messages and send_files() to send files/images.
    Use get_friends() to get friend information and filter by tags.
    Use get_history_messages() to get chat history with automatic loading of more messages.
    """
)

# Initialize WeChat instance
wx = WeChat()

@mcp.tool()
async def get_history_messages(
    who: str,
    min_messages: int = 10,
    max_load_attempts: int = 0,
    exact: bool = False,
    savepic: bool = False,
    savevideo: bool = False,
    savefile: bool = False,
    savevoice: bool = False,
    parseurl: bool = False,
    ctx: Context = None
) -> List[Dict]:
    """
    Get chat history messages for a specific contact or group.
    Automatically loads more messages if needed to reach the minimum count.
    
    Args:
        who: The contact or group name to get messages from
        min_messages: Minimum number of messages to try to load (default: 10)
        max_load_attempts: Maximum number of times to try loading more messages (default: 3)
        exact: Whether to use exact matching for the contact/group name
        savepic: Whether to save chat images
        savevideo: Whether to save chat videos
        savefile: Whether to save chat files
        savevoice: Whether to save voice messages as text
        parseurl: Whether to parse URL cards
    
    Returns:
        List of message dictionaries containing:
        - type: Message type (sys, time, self, friend)
        - content: Message content
        - sender: Message sender
        - time: Message time (for time messages)
    """
    try:
        if ctx:
            await ctx.info(f"Getting messages from {who}")
        
        # First switch to the chat
        wx.ChatWith(who=who, exact=exact)
        
        # Get initial messages
        messages = wx.GetAllMessage(
            savepic=savepic,
            savevideo=savevideo,
            savefile=savefile,
            savevoice=savevoice,
            parseurl=parseurl
        )
        
        # Try to load more messages if needed
        load_attempts = 0
        while len(messages) < min_messages and load_attempts < max_load_attempts:
            if ctx:
                await ctx.info(f"Loading more messages (attempt {load_attempts + 1}/{max_load_attempts})")
            
            if not wx.LoadMoreMessage():
                break
            
            # Get updated messages after loading more
            messages = wx.GetAllMessage(
                savepic=savepic,
                savevideo=savevideo,
                savefile=savefile,
                savevoice=savevoice,
                parseurl=parseurl
            )
            load_attempts += 1
        
        # Convert messages to a simpler format
        result = []
        for msg in messages:
            message_info = {
                'type': msg.type,
                'content': msg.content,
                'sender': msg.sender
            }
            
            # Add time for time messages
            if msg.type == 'time':
                message_info['time'] = msg.time
                
            result.append(message_info)
        
        if ctx:
            await ctx.info(f"Retrieved {len(result)} messages from {who}")
        
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to get messages: {str(e)}")
        raise

@mcp.tool()
async def get_friends(
    tags: Optional[List[str]] = None,
    ctx: Context = None
) -> List[Dict[str, str]]:
    """
    Get basic information about WeChat friends, optionally filtered by tags.
    
    Args:
        tags: Optional list of tags to filter friends by. If provided, only returns friends with matching tags.
    
    Returns:
        List of dictionaries containing friend information. Each dictionary includes:
        - nickname: Friend's nickname
        - remark: Friend's remark name (if set)
        - tags: List of tags associated with the friend
    """
    try:
        if ctx:
            await ctx.info("Getting friends list...")
        
        # Get basic friend information
        friends = wx.GetAllFriends()
        
        # Filter by tags if specified
        if tags:
            friends = [
                friend for friend in friends
                if friend['tags'] and any(tag in friend['tags'] for tag in tags)
            ]
        
        if ctx:
            await ctx.info(f"Found {len(friends)} friends" + (f" matching tags {tags}" if tags else ""))
        
        return friends
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to get friends list: {str(e)}")
        raise

@mcp.tool()
async def send_text(
    msg: str,
    who: Optional[str] = None,
    clear: bool = True,
    exact: bool = False,
    ctx: Context = None
) -> str:
    """
    Send a text message to a WeChat contact or group.
    
    Args:
        msg: The message text to send
        who: The contact or group name to send to (defaults to current chat)
        clear: Whether to clear the input box before sending
        exact: Whether to use exact matching for the contact/group name
    
    Returns:
        Success message
    """
    try:
        if ctx:
            await ctx.info(f"Sending message to {who or 'current chat'}")
        
        wx.SendTypingText(
            msg=msg,
            who=who,
            clear=clear,
            exact=exact
        )
        return f"Message sent successfully to {who or 'current chat'}"
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to send message: {str(e)}")
        raise

@mcp.tool()
async def send_files(
    filepath: Union[str, List[str]],
    who: Optional[str] = None,
    exact: bool = False,
    ctx: Context = None
) -> str:
    """
    Send files, images, or videos to a WeChat contact or group.
    
    Args:
        filepath: Path(s) to the file(s) to send
        who: The contact or group name to send to (defaults to current chat)
        exact: Whether to use exact matching for the contact/group name
    
    Returns:
        Success message
    """
    try:
        if ctx:
            await ctx.info(f"Sending files to {who or 'current chat'}")
        
        success = wx.SendFiles(
            filepath=filepath,
            who=who,
            exact=exact
        )
        
        if success:
            return f"Files sent successfully to {who or 'current chat'}"
        else:
            raise Exception("Failed to send files")
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to send files: {str(e)}")
        raise

@mcp.tool()
async def switch_chat(who: str, exact: bool = False, ctx: Context = None) -> str:
    """
    Switch to a different WeChat chat window.
    
    Args:
        who: The contact or group name to switch to
        exact: Whether to use exact matching for the contact/group name
    
    Returns:
        Success message
    """
    try:
        if ctx:
            await ctx.info(f"Switching to chat with {who}")
        
        result = wx.ChatWith(who=who, exact=exact)
        return f"Switched to chat with {result}"
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to switch chat: {str(e)}")
        raise

if __name__ == "__main__":
    mcp.run(transport='sse') 