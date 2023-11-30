#include "Python.h"
#include "structmember.h"
#include <stdbool.h>
#ifdef _WIN32
#include "snf_win.h"
#else // !_WIN32
#include "snf.h"
#endif // !_WIN32
#include "sn3err.h"
#include "status_code.h"

#if defined(_WIN32)
#define SNF_PREFIX(fname) w##fname
#else // !defined(_WIN32)
#define SNF_PREFIX(fname) fname
#endif // !defined(_WIN32)

#ifdef _WIN32
// snf_mfi_unload 윈도우에서는 w버전을 지원하지 않아 mbcs로 인코딩한다.
#define LOCAL_ENCODING "mbcs"
#else // !_WIN32
#define LOCAL_ENCODING NULL
#endif // !_WIN32

//////////////////////////////////////////////////////////////////////////////
// Exception
//////////////////////////////////////////////////////////////////////////////

static PyObject *SNFError;

// snf_xxx 함수를 호출하면 snf 자체 에러코드를 리턴하는데, 이를 예외로 던지기 위해 사용한다.
// python에서 예외를 잡고 값을 사용하는 방법은 다음과 같이 사용한다.
/*
Python 코드:
from pympower_ext._snf as snf
try:
	mfi = snf.SN3MFI()
	mfi.fopen('')
except snf.SNFError as e:
	error_func, error_code = e.args
	print(f'error_func={error_func}, error_code={error_code}')

결과 값:
error_func=snf_mfi_wfopen, error_code=10510
*/
static void raise_SNFError(const char *function_name, int error_code)
{
	PyObject *err_args = PyTuple_New(2);
	PyObject *function_name_obj = PyUnicode_FromString(function_name);
	PyObject *error_code_obj = PyLong_FromLong(error_code);

	PyTuple_SetItem(err_args, 0, function_name_obj);
	PyTuple_SetItem(err_args, 1, error_code_obj);
	PyErr_SetObject(SNFError, err_args);

	Py_DECREF(err_args);
}

//////////////////////////////////////////////////////////////////////////////
// MFI 클래스
//////////////////////////////////////////////////////////////////////////////

typedef struct _MFI
{
	PyObject_HEAD
	SN3MFI *mfi;
} MFI;

static PyTypeObject MFI_Type;

static PyObject *MFI_New()
{
	PyObject *mfiobj;
	PyObject *arg_list;

	arg_list = Py_BuildValue("()");
	if(NULL == arg_list)
	{
		return NULL;
	}
	mfiobj = PyObject_Call((PyObject *) &MFI_Type, arg_list, NULL);
	Py_DECREF(arg_list);
	return mfiobj;
}

static int MFI___init__(PyObject *self, PyObject *args, PyObject *kwargs)
{
	if(!_PyArg_NoPositional("MFI", args) && !_PyArg_NoKeywords("MFI", kwargs))
	{
		return -1;
	}

    return 0;
}

static void MFI_dealloc(MFI *self)
{
	if(self->mfi)
	{
		SNF_PREFIX(snf_mfi_fclose)(self->mfi);
	}

	Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *MFI_fopen(PyObject *selfobj, PyObject *args)
{
	MFI *self;
	int snf_result;
#ifdef _WIN32
	static const char *args_format = "u";
	wchar_t *path;
#else // !_WIN32
	static const char *args_format = "s";
	char *path;
#endif // !_WIN32

	self = (MFI*) selfobj;

	if(!PyArg_ParseTuple(args, args_format, &path))
	{
		return NULL;
	}

#ifdef _WIN32
	snf_result = wsnf_mfi_wfopen(path, &self->mfi);
#else // !_WIN32
	snf_result = snf_mfi_fopen(path, &self->mfi);
#endif // !_WIN32
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_mfi_wfopen", snf_result);
		return NULL;
	}

    Py_RETURN_NONE;
}

static PyObject *MFI_unload(PyObject *selfobj, PyObject *args)
{
	MFI *self;
	char *path;
	int snf_result;

	self = (MFI*) selfobj;

	if(!PyArg_ParseTuple(args, "es", LOCAL_ENCODING, &path))
	{
		return NULL;
	}

	snf_result = SNF_PREFIX(snf_mfi_unload)(self->mfi, path);
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_mfi_unload", snf_result);
		PyMem_Free(path);
		return NULL;
	}

	PyMem_Free(path);

	Py_RETURN_NONE;
}

static PyObject *MFI_fclose(PyObject *selfobj, PyObject *unused_args)
{
	MFI *self;
	char *path;
	int snf_result;

	self = (MFI*) selfobj;

	snf_result = SNF_PREFIX(snf_mfi_fclose)(self->mfi);
	self->mfi = NULL;
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_mfi_fclose", snf_result);
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyObject *MFT_fmt_detect(PyObject *selfobj, PyObject *unused_args)
{
	MFI *self;
	char *path;
	int snf_result;
	int format;

	self = (MFI*) selfobj;

	snf_result = SNF_PREFIX(snf_fmt_detect_m)(self->mfi, &format);
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_fmt_detect_m", snf_result);
		return NULL;
	}

	return PyLong_FromLong(format);
}

static PyMethodDef MFI_methods[] =
{
	{ "fopen", MFI_fopen, METH_VARARGS, "" },
	{ "unload", MFI_unload, METH_VARARGS, "" },
	{ "fclose", MFI_fclose, METH_NOARGS, "" },
	{ "fmt_detect", MFT_fmt_detect, METH_NOARGS, "" },
	{ NULL, NULL, 0, NULL }
};

static PyTypeObject MFI_Type = {
	PyVarObject_HEAD_INIT(NULL, 0) "pympower_ext._snf.SN3MFI",	/* tp_name */
	sizeof(MFI),						/* tp_basicsize */
	0,									/* tp_itemsize */
	(destructor) MFI_dealloc,			/* tp_dealloc */
	0,									/* tp_vectorcall_offset */
	0,									/* tp_getattr */
	0,									/* tp_setattr */
	0,									/* tp_as_async */
	0,									/* tp_repr */
	0,									/* tp_as_number */
	0,									/* tp_as_sequence */
	0,									/* tp_as_mapping */
	0,									/* tp_hash  */
	0,									/* tp_call */
	0,									/* tp_str */
	0,									/* tp_getattro */
	0,									/* tp_setattro */
	0,									/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,									/* tp_clear */
	0,									/* tp_richcompare */
	0,									/* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	MFI_methods,						/* tp_methods */
	0,									/* tp_members */
	0,									/* tp_getset */
	0,									/* tp_base */
	0,									/* tp_dict */
	0,									/* tp_descr_get */
	0,									/* tp_descr_set */
	0,									/* tp_dictoffset */
	MFI___init__,						/* tp_init */
	0,									/* tp_alloc */
	PyType_GenericNew,					/* tp_new */
};

//////////////////////////////////////////////////////////////////////////////
// MARKER 클래스
//////////////////////////////////////////////////////////////////////////////

typedef struct _MARKER
{
	PyObject_HEAD
	int state;
	PyObject* marker;
	PyObject* unzipMFI;
	int depth;
	int ret;
} MARKER;

static PyTypeObject MARKER_Type;

static PyObject *MARKER_New()
{
	PyObject *markerobj;
	PyObject *arg_list;

	arg_list = Py_BuildValue("()");
	if(NULL == arg_list)
	{
		return NULL;
	}
	markerobj = PyObject_Call((PyObject *) &MARKER_Type, arg_list, NULL);
	Py_DECREF(arg_list);
	return markerobj;
}

static int MARKER___init__(PyObject *selfobj, PyObject *args, PyObject *kwargs)
{
	if(!_PyArg_NoPositional("MARKER", args) && !_PyArg_NoKeywords("MARKER", kwargs))
	{
		return -1;
	}

    return 0;
}

static void MARKER_dealloc(MARKER *self)
{
	Py_XDECREF(self->marker);
	Py_XDECREF(self->unzipMFI);

	Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyMemberDef MARKER_members[] =
{
	{ "state", T_INT, offsetof(MARKER, state), READONLY, NULL },
	{ "marker", T_OBJECT, offsetof(MARKER, marker), READONLY, NULL },
	{ "unzipMFI", T_OBJECT, offsetof(MARKER, unzipMFI), READONLY, NULL },
	{ "depth", T_INT, offsetof(MARKER, depth), READONLY, NULL },
	{ "ret", T_INT, offsetof(MARKER, ret), READONLY, NULL },
	{ NULL }
};

static PyTypeObject MARKER_Type = {
	PyVarObject_HEAD_INIT(NULL, 0) "pympower_ext._snf.SN3MARKER",	/* tp_name */
	sizeof(MARKER),						/* tp_basicsize */
	0,									/* tp_itemsize */
	(destructor) MARKER_dealloc,		/* tp_dealloc */
	0,									/* tp_vectorcall_offset */
	0,									/* tp_getattr */
	0,									/* tp_setattr */
	0,									/* tp_as_async */
	0,									/* tp_repr */
	0,									/* tp_as_number */
	0,									/* tp_as_sequence */
	0,									/* tp_as_mapping */
	0,									/* tp_hash  */
	0,									/* tp_call */
	0,									/* tp_str */
	0,									/* tp_getattro */
	0,									/* tp_setattro */
	0,									/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,									/* tp_clear */
	0,									/* tp_richcompare */
	0,									/* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	0,									/* tp_methods */
	MARKER_members,						/* tp_members */
	0,									/* tp_getset */
	0,									/* tp_base */
	0,									/* tp_dict */
	0,									/* tp_descr_get */
	0,									/* tp_descr_set */
	0,									/* tp_dictoffset */
	MARKER___init__,					/* tp_init */
	0,									/* tp_alloc */
	PyType_GenericNew,					/* tp_new */
};

//////////////////////////////////////////////////////////////////////////////
// BUF 클래스
//////////////////////////////////////////////////////////////////////////////

typedef struct _BUF
{
	PyObject_HEAD
	// 사용자가 BUF.fopen 함수를 사용해 파일을 open한 경우 true로 설정한다.
	// 콜백 함수에서 들어온 경우에는 false로 설정한다.
	// 사용자가 fopen하지 않은 파일을 fclose하는지 검사하는 용도로 사용한다.
	bool user_open;
	SN3BUF *buf;
	// SNF는 snf_buf_user_func를 1글자를 추출할 때 마다 호출하는데,
	// 그대로 파이썬 콜백을 호출하면 마찬가지로 1글자씩 메모리를 할당하고
	// 콜백 호출하고 메모리 해제하는 방식으로 동작한다.
	// 파이썬 콜백을 호출할 때는 일정 크기만큼 버퍼가 차면 파이썬 콜백을
	// 호출하는 방식으로 변경했다. 이 때, 캐시를 하는동안 텍스트 추출이 끝나면
	// 텍스트 추출 완료 후 사용자 콜백을 한 번 더 호출해 캐시된 데이터를
	// 처리할 수 있도록 하기위해 cached 값을 확인한다.
	bool cached;
	size_t callback_chunk_size;

	PyObject *user_func;
	PyObject *user_data;
	PyObject *marker_func;
	PyObject *marker_data;
} BUF;

static PyTypeObject BUF_Type;

static int BUF___init__(PyObject *selfobj, PyObject *args, PyObject *kwargs)
{
	BUF *self;
	int snf_result;
	Py_ssize_t callback_chunk_size = 4096;

	static const char * const _keywords[] = {"callback_chunk_size", NULL};

	self = (BUF*) selfobj;

	if(!PyArg_ParseTupleAndKeywords(args, kwargs, "|n", _keywords, &callback_chunk_size))
	{
		return -1;
	}

	snf_result = SNF_PREFIX(snf_buf_init)(&self->buf);
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_buf_init", snf_result);
		return -1;
	}

	self->cached = false;
	// TODO: 사용자가 옵션 변경할 수 있게 수정할 것
	self->callback_chunk_size = callback_chunk_size;

	return 0;
}

static void BUF_dealloc(BUF *self)
{
	if(self->user_open && self->buf)
	{
		SNF_PREFIX(snf_buf_free)(self->buf);
	}

	Py_XDECREF(self->user_func);
	Py_XDECREF(self->user_data);
	Py_XDECREF(self->marker_func);
	Py_XDECREF(self->marker_data);

	Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *BUF_isempty(PyObject *selfobj, PyObject *args)
{
	BUF *self;

	self = (BUF* ) selfobj;

	if(!_PyArg_NoPositional("isempty", args))
	{
		return NULL;
	}

	if(1 == SNF_PREFIX(snf_buf_isempty)(self->buf))
	{
		Py_RETURN_TRUE;
	}
	else
	{
		Py_RETURN_FALSE;
	}
}

static PyObject *BUF_size(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	PyObject *return_value;
	size_t size;

	self = (BUF* ) selfobj;

	if(!_PyArg_NoPositional("size", args))
	{
		return NULL;
	}

	size = SNF_PREFIX(snf_buf_size)(self->buf);
	return_value = PyLong_FromSize_t(size);
	if(NULL == return_value)
	{
		PyErr_NoMemory();
		return NULL;
	}

	return return_value;
}

static PyObject *BUF_get_utf8_len(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	PyObject *return_value;
	size_t utf8_len;

	self = (BUF* ) selfobj;

	if(!_PyArg_NoPositional("get_utf8_len", args))
	{
		return NULL;
	}

	utf8_len = SNF_PREFIX(snf_buf_get_utf8_len)(self->buf);
	return_value = PyLong_FromSize_t(utf8_len);
	if(NULL == return_value)
	{
		PyErr_NoMemory();
		return NULL;
	}

	return return_value;
}

static PyObject *BUF_clear(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	int snf_result;

	self = (BUF* ) selfobj;

	if(!_PyArg_NoPositional("clear", args))
	{
		return NULL;
	}

	snf_result = SNF_PREFIX(snf_buf_clear)(self->buf);
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_buf_clear", snf_result);
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyObject *BUF_append(PyObject *selfobj, PyObject *args)
{
	PyErr_SetNone(PyExc_NotImplementedError);
	return NULL;
}

static PyObject *BUF_unload(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	int snf_result;

#ifdef _WIN32
	static const char *args_format = "ui";
	wchar_t *path;
#else // !_WIN32
	static const char *args_format = "si";
	char *path;
#endif // !_WIN32
	int encoding;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, args_format, &path, &encoding))
	{
		return NULL;
	}

#ifdef _WIN32
	snf_result = wsnf_buf_wunload(self->buf, (__ucs2 *) path, encoding);
#else // !_WIN32
	snf_result = snf_buf_unload(self->buf, path, encoding);
#endif // !_WIN32
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_buf_unload", snf_result);
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyObject *BUF_get_text(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	PyObject *bytes_buffer;
	PyObject *return_value;
	int size = INT_MAX;
	size_t sn3buf_size;
	size_t sn3buf_pos;
	int alloc_size;
    int available_size;
	int size_returned;
	__ucs2 *ucs2_buf;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "|i", &size))
	{
		return NULL;
	}

	sn3buf_size = SNF_PREFIX(snf_buf_size)(self->buf);
	sn3buf_pos = SNF_PREFIX(snf_buf_getpos)(self->buf);
    available_size = sn3buf_size - sn3buf_pos;
	if(0 > available_size)
	{
		// TODO: 에러 처리
	}

	alloc_size = size < available_size ? size : available_size;

	bytes_buffer = PyBytes_FromStringAndSize(NULL, alloc_size * sizeof(Py_UCS2));
	if(NULL == bytes_buffer)
	{
		PyErr_NoMemory();
		return NULL;
	}

	ucs2_buf = PyBytes_AS_STRING(bytes_buffer);
	size_returned = SNF_PREFIX(snf_buf_get_ucs2)(self->buf, ucs2_buf, alloc_size);
	_PyBytes_Resize(&bytes_buffer, size_returned * sizeof(Py_UCS2));

	return_value = PyUnicode_FromEncodedObject(bytes_buffer, "utf16", NULL);
	Py_DECREF(bytes_buffer);
	if(NULL == return_value)
	{
		return NULL;
	}

	return return_value;
}

static void call_snf_buf_user_func(SN3BUF* sn3buf, BUF *buf)
{
	PyObject *callback_returned;

	// TODO: Py_None에 대해 Py_INCREF를 호출해야 하는지 확인
	PyObject *arg_list = PyTuple_Pack(2, buf, buf->user_data ? buf->user_data : Py_None);
	if(NULL == arg_list)
	{
		// TODO: BUF *buf를 통해 에러를 전달할 것.
		SNF_PREFIX(snf_buf_set_user_command)(sn3buf, SN3_USER_STOP);
		return;
	}

	// TODO: 리턴 값 처리
	callback_returned = PyObject_Call(buf->user_func, arg_list, NULL);
	Py_XDECREF(callback_returned);
	Py_DECREF(arg_list);

	buf->cached = false;
}

static void snf_buf_user_func(SN3BUF* sn3buf, BUF *buf)
{
	size_t bufsize;
	size_t bufpos;

	// 파이썬 예외가 발생했음에도 예외를 처리하지 않고 계속 파이썬 코드를 호출하는 것은
	// 에러이므로 파이썬 콜백 함수를 호출하지 않도록 여기서 무조건 리턴한다.
	if(PyErr_Occurred())
	{
		SNF_PREFIX(snf_buf_set_user_command)(sn3buf, SN3_USER_STOP);
		return;
	}

	bufsize = SNF_PREFIX(snf_buf_size)(sn3buf);
	bufpos = SNF_PREFIX(snf_buf_getpos)(sn3buf);
	if(buf->callback_chunk_size > (bufsize - bufpos))
	{
		buf->cached = true;
		return;
	}

	call_snf_buf_user_func(sn3buf, buf);
}

static PyObject *BUF_set_user_func(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	PyObject *user_func;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "O", &user_func))
	{
		return NULL;
	}

	if(!PyCallable_Check(user_func))
	{
		PyErr_SetString(PyExc_TypeError, "the first argument must be callable");
		return NULL;
	}

	Py_INCREF(user_func);
	Py_XDECREF(self->user_func);
	self->user_func = user_func;

	SNF_PREFIX(snf_buf_set_user_func)(self->buf, snf_buf_user_func);
	SNF_PREFIX(snf_buf_set_user_data)(self->buf, self);

	Py_RETURN_NONE;
}

static PyObject *BUF_set_user_data(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	PyObject *user_data;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "O", &user_data))
	{
		return NULL;
	}

	Py_INCREF(user_data);
	Py_XDECREF(self->user_data);
	self->user_data = user_data;

	Py_RETURN_NONE;
}

static PyObject *BUF_set_user_command(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	int user_command;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "i", &user_command))
	{
		return NULL;
	}

	SNF_PREFIX(snf_buf_set_user_command)(self->buf, user_command);

	Py_RETURN_NONE;
}

static int snf_buf_marker_func(SN3BUF *sn3buf, BUF *buf, SN3MARKER *sn3marker)
{
	PyObject *marker_data = NULL;
	PyObject *markerobj = NULL;
	PyObject *marker_returned = NULL;
	int marker_returned_real;
	MARKER *marker;
	int byteorder = 0; // native order

	// 파이썬 예외가 발생했음에도 예외를 처리하지 않고 계속 파이썬 코드를 호출하는 것은
	// 에러이므로 파이썬 콜백 함수를 호출하지 않도록 여기서 무조건 리턴한다.
	if(PyErr_Occurred())
	{
		return SN3_USER_STOP;
	}

	if(buf->cached)
	{
		call_snf_buf_user_func(sn3buf, buf);
		if(PyErr_Occurred())
		{
			return SN3_USER_STOP;
		}
	}

	marker_data = buf->marker_data ? buf->marker_data : Py_None;

	markerobj = MARKER_New();
	if(NULL == markerobj)
	{
		goto FUNCTION_ERROR_EXIT;
	}

	marker = (MARKER *) markerobj;

	marker->state = sn3marker->state;
	if(sn3marker->marker)
	{
		marker->marker = PyUnicode_DecodeUTF16(sn3marker->marker, SNF_PREFIX(snf_ucs_wcslen)(sn3marker->marker) * sizeof(__ucs2), NULL, &byteorder);
		if(NULL == marker->marker)
		{
			goto FUNCTION_ERROR_EXIT;
		}
	}
	if(sn3marker->unzipMFI)
	{
		marker->unzipMFI = MFI_New();
		if(NULL == marker->unzipMFI)
		{
			goto FUNCTION_ERROR_EXIT;
		}

		// sn3marker->unzipMFI는 파이선 객체와 생명 주기가 다르다.
		// 따라서 BUF에 MFI 객체를 저장해 두고 cursor와 비슷한 개념으로 사용한다.
		// TODO: 수정 할 것.
		((MFI *) marker->unzipMFI)->mfi = sn3marker->unzipMFI;
	}
	marker->depth = sn3marker->depth;
	marker->ret = sn3marker->ret;

	// TODO: Py_None에 대해 Py_INCREF를 호출해야 하는지 확인
	PyObject *arg_list = PyTuple_Pack(3, buf, marker_data, markerobj);
	if(NULL == arg_list)
	{
		goto FUNCTION_ERROR_EXIT;
	}

	marker_returned = PyObject_Call(buf->marker_func, arg_list, NULL);
	if(marker->unzipMFI)
	{
		// dealloc 함수에서 mfi를 닫지 않도록 NULL로 만든다.
		((MFI *) marker->unzipMFI)->mfi = NULL;
		Py_XDECREF(((MFI *) marker->unzipMFI)->mfi);
	}
	Py_DECREF(arg_list);
	if(PyErr_Occurred())
	{
		Py_XDECREF(marker_returned);
		goto FUNCTION_ERROR_EXIT;
	}

	if(PyLong_Check(marker_returned))
	{
		marker_returned_real = PyLong_AsLong(marker_returned);
		Py_DECREF(marker_returned);
		Py_XDECREF(markerobj);
		return marker_returned_real;
	}
	else
	{
		PyErr_SetString(PyExc_Exception, "marker function return value should be integer.");
		Py_DECREF(marker_returned);
		Py_XDECREF(markerobj);
		return SN3_USER_STOP;
	}

FUNCTION_ERROR_EXIT:
	Py_XDECREF(markerobj);

	return SN3_USER_STOP;
}

static PyObject *BUF_set_marker_func(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	PyObject *marker_func;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "O", &marker_func))
	{
		return NULL;
	}

	if(!PyCallable_Check(marker_func))
	{
		PyErr_SetString(PyExc_TypeError, "the first argument must be callable");
		return NULL;
	}

	Py_INCREF(marker_func);
	Py_XDECREF(self->marker_func);
	self->marker_func = marker_func;

	SNF_PREFIX(snf_buf_set_marker_func)(self->buf, snf_buf_marker_func);
	SNF_PREFIX(snf_buf_set_marker_data)(self->buf, self);

	Py_RETURN_NONE;
}

static PyObject *BUF_set_marker_data(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	PyObject *marker_data;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "O", &marker_data))
	{
		return NULL;
	}

	Py_INCREF(marker_data);
	Py_XDECREF(self->marker_data);
	self->marker_data = marker_data;

	Py_RETURN_NONE;
}

static PyObject *BUF_set_skip_command(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	int skip_command;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "i", &skip_command))
	{
		return NULL;
	}

	SNF_PREFIX(snf_buf_set_skip_command)(self->buf, skip_command);

	Py_RETURN_NONE;
}

static PyObject *BUF_get_skip_command(PyObject *selfobj, PyObject *args)
{
	PyErr_SetNone(PyExc_NotImplementedError);
	return NULL;
}

static PyObject *BUF_set_unknownfile_func(PyObject *selfobj, PyObject *args)
{
	PyErr_SetNone(PyExc_NotImplementedError);
	return NULL;
}

static PyObject *BUF_filter(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	int snf_result;

#ifdef _WIN32
	static const char *args_format = "u|i";
	wchar_t *path;
#else // !_WIN32
	static const char *args_format = "s|i";
	char *path;
#endif // !_WIN32
	int with_page = 0;
	SN3MFI *tempMFI;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, args_format, &path, &with_page))
	{
		return NULL;
	}

	// 윈도우에서는 wsnf_flt_wfilter와 같은 형식의 함수를 제공하지 않기 때문에,
	// wchar_t를 사용하려면 MFI 객체를 생성해 처리한다.
#ifdef _WIN32
	snf_result = wsnf_mfi_wfopen(path, &tempMFI);
#else // !_WIN32
	snf_result = snf_mfi_fopen(path, &tempMFI);
#endif // !_WIN32
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_mfi_wfopen", snf_result);
		return NULL;
	}

	snf_result = SNF_PREFIX(snf_flt_filter_m)(tempMFI, self->buf, with_page);
	if(PyErr_Occurred())
	{
		// 임시 MFI 종료
		SNF_PREFIX(snf_mfi_fclose)(tempMFI);
		return NULL;
	}
	if(self->cached)
	{
		call_snf_buf_user_func(self->buf, self);
		if(PyErr_Occurred())
		{
			// 임시 MFI 종료
			SNF_PREFIX(snf_mfi_fclose)(tempMFI);
			return NULL;
		}
	}
	// 임시 MFI 종료
	SNF_PREFIX(snf_mfi_fclose)(tempMFI);
	if(SN3OK != snf_result && SN3_USER_STOP != snf_result)
	{
		raise_SNFError("snf_flt_filter_m", snf_result);
		return NULL;
	}

	return PyLong_FromLong(snf_result);
}

static PyObject *BUF_filter_m(PyObject *selfobj, PyObject *args)
{
	BUF *self;
	int snf_result;
	PyObject* mfiobj;
	MFI *mfi;
	int with_page = 0;

	self = (BUF* ) selfobj;

	if(!PyArg_ParseTuple(args, "O|i", &mfiobj, &with_page))
	{
		return NULL;
	}

	if(!Py_IS_TYPE(mfiobj, &MFI_Type))
	{
		// TODO: 에러 설정 확인
		return NULL;
	}

	mfi = (MFI *) mfiobj;

	snf_result = SNF_PREFIX(snf_flt_filter_m)(mfi->mfi, self->buf, with_page);
	if(PyErr_Occurred())
	{
		return NULL;
	}
	if(self->cached)
	{
		call_snf_buf_user_func(self->buf, self);
		if(PyErr_Occurred())
		{
			return NULL;
		}
	}
	if(SN3OK != snf_result && SN3_USER_STOP != snf_result)
	{
		raise_SNFError("snf_flt_filter_m", snf_result);
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyMethodDef BUF_methods[] =
{
	{ "isempty", (PyCFunction) BUF_isempty, METH_VARARGS, "" },
	{ "size", (PyCFunction) BUF_size, METH_VARARGS, "" },
	{ "get_utf8_len", (PyCFunction) BUF_get_utf8_len, METH_VARARGS, "" },
	{ "clear", (PyCFunction) BUF_clear, METH_VARARGS, "" },
	{ "append", (PyCFunction) BUF_append, METH_VARARGS, "" },
	{ "unload", (PyCFunction) BUF_unload, METH_VARARGS, "" },
	//{ "putc", (PyCFunction) BUF_putc, METH_VARARGS, "" },
	//{ "put_newline", (PyCFunction) BUF_put_newline, METH_VARARGS, "" },
	//{ "put_space", (PyCFunction) BUF_put_space, METH_VARARGS, "" },
	//{ "peek_start", (PyCFunction) BUF_peek_start, METH_VARARGS, "" },
	//{ "peek_end", (PyCFunction) BUF_peek_end, METH_VARARGS, "" },
	//{ "getch", (PyCFunction) BUF_getch, METH_VARARGS, "" },
	//{ "ungetch", (PyCFunction) BUF_ungetch, METH_VARARGS, "" },
	//{ "get", (PyCFunction) BUF_get, METH_VARARGS, "" },
	//{ "setpos", (PyCFunction) BUF_setpos, METH_VARARGS, "" },
	//{ "getpos", (PyCFunction) BUF_getpos, METH_VARARGS, "" },
	//{ "rewind", (PyCFunction) BUF_rewind, METH_VARARGS, "" },
	{ "get_text", (PyCFunction) BUF_get_text, METH_VARARGS, "" },
	{ "set_user_func", (PyCFunction) BUF_set_user_func, METH_VARARGS, "" },
	{ "set_user_data", (PyCFunction) BUF_set_user_data, METH_VARARGS, "" },
	{ "set_user_command", (PyCFunction) BUF_set_user_command, METH_VARARGS, "" },
	{ "set_marker_func", (PyCFunction) BUF_set_marker_func, METH_VARARGS, "" },
	{ "set_marker_data", (PyCFunction) BUF_set_marker_data, METH_VARARGS, "" },
	{ "set_skip_command", (PyCFunction) BUF_set_skip_command, METH_VARARGS, "" },
	{ "get_skip_command", (PyCFunction) BUF_get_skip_command, METH_VARARGS, "" },
	{ "set_unknownfile_func", (PyCFunction) BUF_set_unknownfile_func, METH_VARARGS, "" },
	{ "filter", (PyCFunction) BUF_filter, METH_VARARGS, "" },
	{ "filter_m", (PyCFunction) BUF_filter_m, METH_VARARGS, "" },
	{ NULL, NULL, 0, NULL }
};

static PyMemberDef BUF_members[] =
{
	{ "user_func", T_OBJECT_EX, offsetof(BUF, user_func), READONLY, NULL },
	{ "user_data", T_OBJECT_EX, offsetof(BUF, user_data), READONLY, NULL },
	{ "marker_func", T_OBJECT_EX, offsetof(BUF, marker_func), READONLY, NULL },
	{ "marker_data", T_OBJECT_EX, offsetof(BUF, marker_data), READONLY, NULL },
	{ NULL }
};

static PyTypeObject BUF_Type = {
	PyVarObject_HEAD_INIT(NULL, 0) "pympower_ext._snf.SN3BUF",	/* tp_name */
	sizeof(BUF),						/* tp_basicsize */
	0,									/* tp_itemsize */
	(destructor) BUF_dealloc,			/* tp_dealloc */
	0,									/* tp_vectorcall_offset */
	0,									/* tp_getattr */
	0,									/* tp_setattr */
	0,									/* tp_as_async */
	0,									/* tp_repr */
	0,									/* tp_as_number */
	0,									/* tp_as_sequence */
	0,									/* tp_as_mapping */
	0,									/* tp_hash  */
	0,									/* tp_call */
	0,									/* tp_str */
	0,									/* tp_getattro */
	0,									/* tp_setattro */
	0,									/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,									/* tp_clear */
	0,									/* tp_richcompare */
	0,									/* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	BUF_methods,						/* tp_methods */
	BUF_members,						/* tp_members */
	0,									/* tp_getset */
	0,									/* tp_base */
	0,									/* tp_dict */
	0,									/* tp_descr_get */
	0,									/* tp_descr_set */
	0,									/* tp_dictoffset */
	BUF___init__,						/* tp_init */
	0,									/* tp_alloc */
	PyType_GenericNew,					/* tp_new */
};

//////////////////////////////////////////////////////////////////////////////
// SUM 클래스
//////////////////////////////////////////////////////////////////////////////

typedef struct _SUM
{
	PyObject_HEAD
	SN3SUM *sum;
} SUM;

static PyTypeObject SUM_Type;

static int SUM___init__(PyObject *self, PyObject *args, PyObject *kwargs)
{
	return -1;
}

static void SUM_dealloc(SUM *self)
{
	if(self->sum)
	{
		SNF_PREFIX(snf_sum_free)(self->sum);
	}

	Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *SUM_unload(PyObject *selfobj, PyObject *const *args, Py_ssize_t nargs)
{
	PyErr_SetNone(PyExc_NotImplementedError);
	return NULL;
}

static PyObject *SUM_docinfo(PyObject *selfobj, PyObject *const *args, Py_ssize_t nargs)
{
	PyErr_SetNone(PyExc_NotImplementedError);
	return NULL;
}

static PyMethodDef SUM_methods[] =
{
	{ "unload", (PyCFunction) SUM_unload, METH_NOARGS, ""},
	{ "docinfo", (PyCFunction) SUM_docinfo, METH_NOARGS, ""},
	{ NULL, NULL, 0, NULL }
};

static PyTypeObject SUM_Type = {
	PyVarObject_HEAD_INIT(NULL, 0) "pympower_ext._snf.SN3SUM",	/* tp_name */
	sizeof(SUM),						/* tp_basicsize */
	0,									/* tp_itemsize */
	(destructor) SUM_dealloc,			/* tp_dealloc */
	0,									/* tp_vectorcall_offset */
	0,									/* tp_getattr */
	0,									/* tp_setattr */
	0,									/* tp_as_async */
	0,									/* tp_repr */
	0,									/* tp_as_number */
	0,									/* tp_as_sequence */
	0,									/* tp_as_mapping */
	0,									/* tp_hash  */
	0,									/* tp_call */
	0,									/* tp_str */
	0,									/* tp_getattro */
	0,									/* tp_setattro */
	0,									/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,									/* tp_clear */
	0,									/* tp_richcompare */
	0,									/* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	SUM_methods,						/* tp_methods */
	0,									/* tp_members */
	0,									/* tp_getset */
	0,									/* tp_base */
	0,									/* tp_dict */
	0,									/* tp_descr_get */
	0,									/* tp_descr_set */
	0,									/* tp_dictoffset */
	SUM___init__,						/* tp_init */
	0,									/* tp_alloc */
	PyType_GenericNew,					/* tp_new */
};

//////////////////////////////////////////////////////////////////////////////
// ARFILIST 클래스
//////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////
// SNF 모듈
//////////////////////////////////////////////////////////////////////////////

PyDoc_STRVAR(module_doc,
"Mpower 10.0 snf extension"
);

// snf_gbl_setcfg함수와 이름이 동일해지는 문제가 있어 앞에 _를 붙였다.
static PyObject *_snf_gbl_setcfg(PyObject *module, PyObject *args)
{
	char *pKeyStr;
	__uint64 file_type;
	__uint64 option;
	size_t base_buffer_size;

	if(!PyArg_ParseTuple(args, "zKKn", &pKeyStr, &file_type, &option, &base_buffer_size))
	{
		return NULL;
	}

	SNF_PREFIX(snf_gbl_setcfg)(pKeyStr, file_type, option, base_buffer_size);

	Py_RETURN_NONE;
}

static PyObject * _snf_gbl_setcfgEx(PyObject *module, PyObject *args)
{
	return NULL;
}

static PyObject *_snf_fmt_detect(PyObject *module, PyObject *args)
{
#ifdef _WIN32
	static const char *args_format = "u";
	wchar_t *path;
#else // !_WIN32
	static const char *args_format = "s";
	char *path;
#endif // !_WIN32
	int snf_result;
	int format;

	if(!PyArg_ParseTuple(args, args_format, &path))
	{
		return NULL;
	}

#ifdef _WIN32
	snf_result = wsnf_fmt_wdetect(path, &format);
#else // !_WIN32
	snf_result = snf_fmt_detect(path, &format);
#endif // !_WIN32
	if(SN3OK != snf_result)
	{
		raise_SNFError("snf_fmt_detect", snf_result);
		return NULL;
	}

	return PyLong_FromLong(format);
}

static PyObject *_snf_fmt_format_name(PyObject *module, PyObject *args)
{
	int snf_result;
	int format;
	char *format_name;

	if(!PyArg_ParseTuple(args, "i", &format))
	{
		return NULL;
	}

	format_name = SNF_PREFIX(snf_fmt_format_name)(format);

	return PyUnicode_FromString(format_name);
}

static PyObject *_snf_fmt_formatNameByCode(PyObject *module, PyObject *args)
{
	int snf_result;
	int format_code;
	char *format_name;

	if(!PyArg_ParseTuple(args, "i", &format_code))
	{
		return NULL;
	}

	format_name = SNF_PREFIX(snf_fmt_formatNameByCode)(format_code);

	return PyUnicode_FromString(format_name);
}

static PyObject *_snf_fmt_isFilterFormat(PyObject *module, PyObject *args)
{
	char *path;
	int filter_format;

	if(!PyArg_ParseTuple(args, "s", &path))
	{
		return NULL;
	}

	filter_format = SNF_PREFIX(snf_fmt_isFilterFormat)(path);

	if(1 == filter_format)
	{
		Py_RETURN_TRUE;
	}
	else
	{
		Py_RETURN_FALSE;
	}
}

static PyObject *_snf_error_code_to_status_code(PyObject *module, PyObject *args)
{
	int snf_error_code;
    int status_code;

	if(!PyArg_ParseTuple(args, "i", &snf_error_code))
	{
		return NULL;
	}

    status_code = convertSynapErrorToMpiislError(snf_error_code);

	return PyLong_FromLong(status_code);
}

static PyMethodDef snf_methods[] = {
    { "snf_gbl_setcfg",  _snf_gbl_setcfg, METH_VARARGS, "" },
	{ "snf_gbl_setcfgEx",  _snf_gbl_setcfgEx, METH_VARARGS, "" },
	{ "snf_fmt_detect",  _snf_fmt_detect, METH_VARARGS, "" },
	{ "snf_fmt_format_name", _snf_fmt_format_name, METH_VARARGS, "" },
	{ "snf_fmt_formatNameByCode", _snf_fmt_formatNameByCode, METH_VARARGS, "" },
	{ "snf_fmt_isFilterFormat", _snf_fmt_isFilterFormat, METH_VARARGS, "" },
    { "snf_error_code_to_status_code", _snf_error_code_to_status_code, METH_VARARGS, "" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"pympower_ext._snf",
	module_doc,
	0,
	snf_methods,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit__snf()
{
	PyObject *module = PyModule_Create(&moduledef);
	if (NULL == module)
	{
		return NULL;
	}

	SNFError = PyErr_NewException("pympower_ext._snf.SNFError", NULL, NULL);
	Py_XINCREF(SNFError);
	if(0 > PyModule_AddObject(module, "SNFError", SNFError))
	{
		Py_XDECREF(SNFError);
		Py_CLEAR(SNFError);
		Py_DECREF(module);
		return NULL;
	}

#define ADD_TYPE(type)									\
	if(0 > PyModule_AddType(module, type))				\
	{													\
		goto FUNCTION_ERROR_EXIT;						\
	}

	ADD_TYPE(&MFI_Type)
	ADD_TYPE(&MARKER_Type)
	ADD_TYPE(&BUF_Type)
	ADD_TYPE(&SUM_Type)
	//ADD_TYPE(&ARFILIST_Type)

	return module;

FUNCTION_ERROR_EXIT:
	Py_DECREF(module);
	return NULL;
}
