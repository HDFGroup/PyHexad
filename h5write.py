
import pyxll
from pyxll import xl_arg_doc, xl_func, xl_macro
import h5py

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "The location of the object (attribute owner).")
@xl_arg_doc("data", "The data to be written.")
@xl_arg_doc("start", "The index of the first element to be read.")
@xl_arg_doc("count", "The number of elements to be read along each dimension. Inf - read until the end of the coresponding dimension.")
@xl_arg_doc("stride", "The interelement spacing along each dataset extent.")
#
@xl_func("string filename, string datasetname, numpy_array data, string start, string count, string stride: void")
#
def h5write(filename, datasetname, data, start=None, count=None, stride=None):
    """(partially) writes the value of an HDF5 dataset"""

    # get the address of the calling cell using xlfCaller
    caller = pyxll.xlfCaller()
    address = caller.address

    # the update is done asynchronously so as not to block some
    # versions of Excel by updating the worksheet from a worksheet function
    def update_func():
        xl = xl_app()
        range = xl.Range(address)

        # get the cell below and expand it to rows x cols
        #range = xl.Range(range.Resize(2, 1), range.Resize(rows+1, cols))

        # and set the range's value
        #range.Value = value

    # kick off the asynchronous call the update function
    pyxll.async_call(update_func)

    return address
