#include <Python.h>
#include <unistd.h>

static PyObject * bar(PyObject *self, PyObject *args)
{
    const char *command;
    char* cwd;
    char buff[1000];

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;

    cwd = getcwd(buff, 1000);
    printf("My working directory in %s.\n", cwd);

    return Py_BuildValue("s", cwd);
}

//~ static PyObject * bar(PyObject *self, PyObject *args)
//~ {
    //~ PyObject* py_obj;
    //~ PyObject* py_seq;
    //~ int i, len;
//~
    //~ if (!PyArg_ParseTuple(args, "O", &py_obj))
        //~ return NULL;
    //~ py_seq = PySequence_Fast(py_obj, "expected a sequence");
    //~ len = PySequence_Size(py_obj);
//~
    //~ float float_arg_array[len];
//~
    //~ for (i = 0; i < len; i++) {
        //~ float_arg_array[i] = PyFloat_AsFloat(PySequence_Fast_GET_ITEM(py_seq, i));
        //~ printf("%ith element is: %f\n", i, double_arg_array[i]);
    //~ }
    //~ Py_DECREF(float_arg_array);
//~
//~
    //~ // Тут у вас есть массив double_arg_array с аргументами типа float
//~
//~
    //~ //
//~
    //~ PyObject* result_tuple = PyTuple_New(len);
    //~ for (i = 0; i < len; i++) {
        //~ PyTuple_SetItem(result_tuple, i, PyFloat_FromDouble(float_arg_array[i]));
    //~ }
    //~ return result_tuple;
//~ }

static PyMethodDef foomodule_funcs[] = {
    {"bar", (PyCFunction)bar, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef foomodule = {
    PyModuleDef_HEAD_INIT,
    "foomodule",
    NULL,
    -1,
    foomodule_funcs
};

PyMODINIT_FUNC
PyInit_foomodule(void)
{
    return PyModule_Create(&foomodule);
}
