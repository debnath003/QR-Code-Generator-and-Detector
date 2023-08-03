from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import filedialog as fd
import qrcode
import cv2

 # the function for generating the QR Code
def generate():
    qrcode_data = str(data_entry.get())
    qrcode_name = str(filename_entry.get())
    if qrcode_name == '':
        showerror(title='Error', message='An error occurred' \
                   '\nThe following is ' \
                    'the cause:\n->Empty Filename\n' \
                    'Filename Must Be Filled')
    else:
        # confirm from the user whether to generate QR code or not
        # if askyesno(title='Confirm', message=f'Create a QR Code?'):
            # the try block for generating the QR Code
        try:
                # Creating an instance of QRCode class
            qr = qrcode.QRCode(version = 1, box_size = 6, border = 4)
                # Adding data to the instance 'qr'
            qr.add_data(qrcode_data)
                # this helps with the dimensions of the QR code
            qr.make(fit = True)
                # the name for the QRCode
            name = qrcode_name + '.png'
                # making the QR code
            qrcode_image = qr.make_image(fill_color = 'black', back_color = 'white')
                # saving the QR code
            qrcode_image.save(name)
                # making the Image variable global
            global Image
                # opening the qrcode image file
            Image = PhotoImage(file=f'{name}')
                # displaying the image on the canvas via the image label
            img_label1.config(image=Image)
                # the button for resetting or clearing the QR code image on the canvas
            resetbutton.config(state=NORMAL, command= reset)
            # this will catch all the errors that might occur
        except:
            showerror(title='Error', message='Give Valid Filename!')

def reset():
    # if askyesno(title= 'Reset?', message= 'Want To Reset?'):
    img_label1.config(image= '')
    resetbutton.config(state= DISABLED)

# the function to detect the QR codes
def detect():
    # getting the image file from the file entry via get() function
    image_file = fileentry.get()
    # checking if the image_file is empty
    if image_file == '':
        # show error when the image_file entry is empty
        showerror(title='Error', message='Please provide a QR Code image file to detect.')
    # executes when the image_file is not empty
    else:
        # code inside the try will detect the QR codes
        try:
            # reading the image file with cv2
            qr_img = cv2.imread(f'{image_file}')
            if qr_img is None:
                raise Exception("Invalid image file. The file may not be an image or may not contain a valid QR code.")
            # using the QRCodeDetector() function
            qr_detector = cv2.QRCodeDetector()
            # making the qrcode_image global
            global qrcode_image
            # opening the qrcode_image using the PhotoImage
            qrcode_image = PhotoImage(file=f'{image_file}')
            # displaying the image via the image label
            img_label2.config(image=qrcode_image)
            # using the detectAndDecode() function detect and decode the QR code
            data, pts, st_code = qr_detector.detectAndDecode(qr_img)
            # displaying data on the data_label
            if data is not None and len(data) > 0:
                data_label.config(text=data)
            else:
                showerror(title='Error', message='No QR Code detected.')
        # this catches any errors that might occur
        except Exception as e:
            showerror(title='Error', message=str(e))

def openfilebutton():
    # This function is called when the "Browse" button is clicked.
    # It opens a file dialog and returns the selected file path.
    name = fd.askopenfilename()
    fileentry.delete(0, END)
    fileentry.insert(0, name)

# both of the windows
window = Tk()
window.title("QR Code Generator and Detector")
window.geometry('700x500')
window.resizable(height=FALSE, width=FALSE)
#window.protocol('DELETE_THE_WINDOW', close())

# label configuration in naming and buttons
label_style = ttk.Style()
label_style.configure('TLabel', foreground= "#000000", font= ('OCR A Extended', 12))
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 16))
button_style = ttk.Style()
button_style.configure('TButton', foreground= '#000000', font= ('DotumChe', 9))

# tab creation
tab_ctrl = ttk.Notebook(window)
firsttab = ttk.Frame(tab_ctrl)
secondtab = ttk.Frame(tab_ctrl)
tab_ctrl.add(firsttab, text= 'CODE GENERATION')
tab_ctrl.add(secondtab, text= 'CODE DETECTION')
tab_ctrl.pack(expand= 1, fill= "both")

# windows on both tabs
firstcanvas = Canvas(firsttab, width=750, height=580)
firstcanvas.pack()
secondcanvas = Canvas(secondtab, width=750, height=580)
secondcanvas.pack()

# first windows' creation
img_label1 = Label(window)
firstcanvas.create_window(250, 150, window= img_label1)

# data
qrdata_label = ttk.Label(window, text= 'QRCODE DATA: ', style= 'TLabel')
data_entry = ttk.Entry(window, width=55, style= 'TEntry')
firstcanvas.create_window(70, 340, window= qrdata_label)
firstcanvas.create_window(300, 340, window= data_entry)

filename_label = ttk.Label(window, text='FILE NAME: ', style='TLabel')
filename_entry = ttk.Entry(width=55, style='TEntry')
firstcanvas.create_window(84, 370, window=filename_label)
firstcanvas.create_window(300, 370, window=filename_entry)

# firstcanvas buttons
resetbutton = ttk.Button(window, text= 'RESET', style= 'TButton', state= DISABLED)
generatebutton = ttk.Button(window, text= 'GENERATE', style= 'TButton', command=generate)
firstcanvas.create_window(310, 400, window= resetbutton)
firstcanvas.create_window(430, 400, window= generatebutton)

# secondcanvas window
img_label2 = Label(window)
data_label = ttk.Label(window)
secondcanvas.create_window(260, 160, window=img_label2)
secondcanvas.create_window(260, 320, window=data_label)

# data
filename = ttk.Label(window, text='FILE PATH:', style='TLabel')
fileentry = ttk.Entry(window, width=70, style='TEntry')
secondcanvas.create_window(65, 390, window=filename)
secondcanvas.create_window(330, 390, window=fileentry)

# browse button
browse_button = ttk.Button(window, text='BROWSE', style='TButton', command=openfilebutton)
secondcanvas.create_window(596, 390, window=browse_button)

# secondcanvas button
detect = ttk.Button(window, text='DETECT', style='TButton', command=detect)
secondcanvas.create_window(58, 420, window=detect)

window.mainloop()
