from utilityai.core import infer
import inspect
from typing import Any, Optional

def message(text: str, conversation: list = [], attachment: Optional[Any] = None, verbose: int = 1, option: Optional[int] = None):
    
    def pandas_info(df):
        info = {}

        if df.empty:
            info['empty'] = True
            return info
        
        try:
            info['dtypes'] = df.dtypes.to_dict()
        except:
            pass
        
        try:
            info['shape'] = df.shape
        except:
            pass
        
        try:
            info['head'] = df.head(1).to_dict(orient='records')
        except:
            pass

        try:
            info['describe'] = df.describe().to_dict()
        except: 
            pass
        
        try:
            info['missing_values'] = df.isnull().sum().to_dict()
        except:
            pass
        
        return info
    
    def numpy_info(array, sample_size=10):
        info = {}

        if array.size == 0:
            info['empty'] = True
            return info
        
        try:
            info['shape'] = array.shape
        except: 
            pass
        
        try:
            info['dtype'] = str(array.dtype)
        except: 
            pass
        
        try:
            info['mean'] = array.mean().item()
        except: 
            pass
        
        try:
            info['median'] = np.median(array).item()
        except: 
            pass
        
        try:
            info['min'] = array.min().item()
        except: 
            pass
        
        try:
            info['max'] = array.max().item()
        except: 
            pass
        
        try:
            info['std_dev'] = array.std().item()
        except: 
            pass

        return info
    
    def pytorch_info(tensor):
        info = {}

        try:
            info["data_type"] = str(tensor.dtype)
        except:
            pass
        
        try:
            info["shape"] = tuple(tensor.shape)
        except:
            pass
            
        try:
            info["size"] = tensor.numel()
        except:
            pass
            
        try:
            info["device"] = str(tensor.device)
        except:
            pass
            
        try:
            info["requires_grad"] = tensor.requires_grad
        except:
            pass
            
        try:
            info["is_empty"] = tensor.numel() == 0
        except:
            pass
        
        return info

    if not isinstance(text, str):
        raise TypeError("text must be a str")

    if not isinstance(conversation, list):
        raise TypeError("conversation must be a list")
    if len(conversation) > 0:
        for item in conversation:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError("Each element of the conversation list must be a tuple with two elements")
    if not isinstance(verbose, int) or verbose not in {0, 1}:
        raise ValueError("verbose must be an integer either 0, 1")
    
    if attachment is not None:
        found_type = False
        if callable(attachment):
            function_source_code = inspect.getsource(attachment)
            text = function_source_code + "\n" + text
        else:
            try:
                import pandas as pd
                if isinstance(attachment, pd.DataFrame):
                    introduction = "pandas dataframe:" + "\n"
                    attachment_info = pandas_info(attachment)
                    text = introduction + str(attachment_info) + "\n" + text
                    found_type = True
            except:
                pass
            if not found_type:
                try:
                    import numpy as np
                    if isinstance(attachment, np.ndarray):
                        introduction = "numpy array:" + "\n"
                        attachment_info = numpy_info(attachment)
                        text = introduction + str(attachment_info) + "\n" + text
                        found_type = True
                except:
                    pass
                if not found_type:
                    try:
                        import torch
                        if isinstance(attachment, torch.Tensor):
                            introduction = "pytorch tensor:" + "\n"
                            attachment_info = pytorch_info(attachment)
                            text = introduction + str(attachment_info) + "\n" + text
                            found_type = True
                    except:
                        pass
                    if not found_type:
                        print("attachment type detection failed")

    conversation_new = conversation[:]
    conversation_new.append((text, None))
    conversation_new = conversation_new[-10:]
    response = infer(conversation_new, verbose=verbose, option=option)
    conversation_new[-1] = (text, response)

    return response, conversation_new
