TITLE Intern Mistake Corrector    (proj6_haneyth.asm)

; Author: Tom Haney
; Last Modified: 06Jun25
; OSU email address: haneyth@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: 6               Due Date: 08Jun25
; Description: Reads temperature measurements from a user-specified file and prints them in reverse order.
;	The program exhibits use of macros for displaying strings and characters, and for getting input from
;	the user. Procedures are also used, for parsing integers from strings and for printing an array in
;	reverse. These elements are combined to display the temperature measurements in corrected order
;	(that being the opposite of the order in the file) to the terminal.

INCLUDE Irvine32.inc

; -----------------------------------------------------------------------------------------------------------
; Name: mGetString
; Description: Displays a prompt for the user to the console, and then saves the user's input to memory.
; Preconditions:	None
; Postconditions:	Prompt printed to console and user's input saved to memory at inputAddress
; Receives:			prompt: A string passed by reference/OFFSET to be output to the console
;					inputAddress: A memory location which will hold the user's input (BYTE array OFFSET)
;					maxLength: The maximum length of string which can be stored at inputAdddress
;					bytesRead: The number of bytes the user entered (the length of the string
; Returns:			inputAddress and bytesRead updated from user inputs
; -----------------------------------------------------------------------------------------------------------
mGetString MACRO prompt, inputAddress, maxLength, bytesRead
	PUSH  EAX	; Preserve registers used
	PUSH  ECX
	PUSH  EDX

	; Display the prompt with the mDisplayString macro
	mDisplayString prompt

	; Get user input
	MOV   ECX, maxLength
	MOV   EDX, inputAddress
	CALL  ReadString
	MOV   bytesRead, EAX

	; Add newline for readability
	CALL  CrLf

	POP  EDX	; Restore registers used
	POP  ECX
	POP  EAX
ENDM

; -----------------------------------------------------------------------------------------------------------
; Name: mDisplayString
; Description: Prints any given string to the console. Does not add any whitespace or new lines, these
;	should be included as part of the string passed in.
; Preconditions:	None
; Postconditions:	String printed to the console
; Receives:			stringAddress: A string passed by reference, in other words its OFFSET
; Returns:			None
; -----------------------------------------------------------------------------------------------------------
mDisplayString MACRO stringAddress
	PUSH  EDX	; Preserve registers used

	; Call WriteString to display the desired text
	MOV   EDX, stringAddress
	CALL  WriteString

	POP   EDX	; Restore registers used
ENDM

; -----------------------------------------------------------------------------------------------------------
; Name: mDisplayChar
; Description: Prints a single character to the console.
; Preconditions:	None
; Postconditions:	Character printed to the console
; Receives:			char: A character. Can accept immediates, constants, or 8-bit registers (e.g. BL)
; Returns:			None
; -----------------------------------------------------------------------------------------------------------
mDisplayChar MACRO char
	PUSH  EAX	; Preserve registers used

	; Call WriteChar to display the desired character
	MOV   AL, char
	CALL  WriteChar

	POP   EAX	; Restore registers used
ENDM

; Constants for determining the number of temps per line and the delimiter within the text file
TEMPS_PER_DAY	= 24
DELIMITER		EQU <",">

; Constant for the maximum allowable length of file name the user may enter
FILENAME_LENGTH = 30

; Constant for the buffer size to be used when the file is read
; (assumes up to 5 characters per temp reading: 1 sign, up to 3 digits, and a delimiter)
BUFFER_SIZE = TEMPS_PER_DAY * 5

.data

; Text declarations used for various statements and prompts within the program.
intro1			BYTE  "Welcome to the intern mistake corrector by Tom Haney!",13,10,0
intro2			BYTE  "This program takes a file of '",DELIMITER,"'-delimited temperature readings",13,10,0
intro3			BYTE  "and prints them to the console in reverse (corrected) order.",13,10,0
filePrompt		BYTE  "Please enter the name of a file holding ASCII-formatted temperature values: ",0
fileNameWrong	BYTE  "The file name appears to have been entered incorrectly! Please try again.",13,10,0
announceTemps	BYTE  "The corrected temperature order is as follows:",13,10,0
sayounara		BYTE  "Goodbye!",0

; Declarations used to retrieve and hold the file name supplied by the user
fileName		BYTE  FILENAME_LENGTH DUP(?)
enteredLength	DWORD ?

; Declarations used to read and store the data from the file (in raw byte form and parsed to numeric form)
fileBuffer		BYTE BUFFER_SIZE DUP(?)
bytesRead		DWORD ?

; Declaration to hold the array of converted temperature values
tempArray		SDWORD TEMPS_PER_DAY DUP(?)

.code
main PROC
	
		; Introduce the program
		mDisplayString	OFFSET intro1
		mDisplayString	OFFSET intro2
		mDisplayString	OFFSET intro3

	_retrieveFileName:
		; Prompt the user for the file name
		mGetString		OFFSET filePrompt, OFFSET fileName, FILENAME_LENGTH, enteredLength

		; Open the file for reading
		MOV   EDX, OFFSET fileName
		CALL  OpenInputFile

		; Check for errors
		CMP   EAX, 0ffffffffh
		JNE   _noError
		mDisplayString  OFFSET fileNameWrong
		JMP   _retrieveFileName

	; If we jump here, the file name was entered correctly
	_noError:
		; Read from the file (EAX already holds the file handle)
		MOV   ECX, BUFFER_SIZE
		MOV   EDX, OFFSET fileBuffer
		CALL  ReadFromFIle

		; Close the file (EAX already holds the file handle)
		CALL  CloseFile

		; Parse temperatures from the file buffer string into an array of temperature values
		PUSH  OFFSET fileBuffer
		PUSH  OFFSET tempArray
		CALL  ParseTempsFromString

		; Tell the user that the corrected order is about to be displayed
		mDisplayString  OFFSET announceTemps

		; Print the temperatures from tempArray to the console in reverse (corrected) order
		PUSH  OFFSET tempArray
		CALL  WriteTempsReverse

		; Say Goodbye
		CALL  CrLf
		CALL  CrLf
		mDisplayString  OFFSET sayounara

	Invoke ExitProcess,0	; exit to operating system
main ENDP

; -----------------------------------------------------------------------------------------------------------
; Name: ParseTempsFromString
; Description: Takes a string of temperatures separated by a DELIMITER, uses string primitives to convert
;	these values to integers, and stores them in tempArray
; Preconditions:	fileBuffer holds the raw ASCII text from the temperature file
; Postconditions:	tempArray populated with integer values for each temperature (order unchanged from file)
; Receives:			[EBP+12]: OFFSET of fileBuffer
;					[EBP+8]:  OFFSET of tempArray
; Returns:			tempArray populated
; -----------------------------------------------------------------------------------------------------------
ParseTempsFromString PROC
	; Using LOCAL, so no need to set up stack frame
	LOCAL currentNum:SDWORD		; To be used in the calculation of each integer

	PUSH  EAX					; Preserve registers used
	PUSH  EBX
	PUSH  ECX
	PUSH  EDX
	PUSH  ESI
	PUSH  EDI

	; Initial Setup
	CLD							; Clear the direction flag to move forward through each array
	MOV   ESI, [EBP+12]			; Point ESI to the fileBuffer
	MOV   EDI, [EBP+8]			; Point EDI to the tempArray
	MOV   currentNum, 0			; Initialize currentNum (local variable) to 0
	MOV   EBX, 0				; EBI used as a "flag" to check if number was negative
	MOV   ECX, TEMPS_PER_DAY	; Using ECX as a counter to decrement how many items need to be converted

	; Loop through each character and evaluate
	_loadNumber:
		LODSB					; Current element of ESI to AL and increment

		; Check for delimiter, if found then this particular integer has been completed
		CMP   AL, DELIMITER
		JE    _delimiterFound

		; Check for minus sign, if so negate the number later
		CMP   AL, "-"
		JNE   _calculateNumber
		INC   EBX				; Set flag for negation
		JMP   _loadNumber

	; If we arrive here, the character must be an integer (unless some unexpected characters are in
	; the file, which I have not added functionality to deal with... fingers crossed?)
	_calculateNumber:
		; Multiply the current integer by 10 to allow the new digit to slide into the ones-place
		PUSH  EAX
		PUSH  ECX
		MOV   EAX, currentNum
		MOV   ECX, 10
		MUL   ECX
		MOV   currentNum, EAX
		POP   ECX
		POP   EAX

		; Convert the ASCII digit to a numerical digit (via the trick showed in the Canvas lecture)
		SUB   EAX, 48

		; Add the now numerical/base-10 digit to the currentNum and move on to the next character
		ADD   currentNum, EAX
		JMP   _loadNumber

	; If we arrive here, the delimiter has been reached and currentNum is the absolute value of the
	; desired integer
	_delimiterFound:
		
		; If EBX != 0, then a negative sign was found and the number must be made negetive
	    CMP   EBX, 0
		JE    _intToArray
		NEG   currentNum

	; Once here, the integer is done being processed and it can be inserted into the tempArray
	_intToArray:
	    MOV   EAX, currentNum
		STOSD

		; Check if we have stored the last value (ECX is the counter, decrement and check against 0)
		DEC   ECX
		CMP   ECX, 0
		JLE   _allNumsLoaded

		; Reset EBX flag, EAX register and currentNum
		MOV   EAX, 0
		MOV   EBX, 0
		MOV   currentNum, 0
		JMP   _loadNumber

	; Once here, ECX has been decremented to 0 and we have converted/stored all temperatures
	_allNumsLoaded:

	POP   EDI					; Restore registers used
	POP   ESI
	POP   EDX
	POP   ECX
	POP   EBX
	POP   EAX

	; LOCAL was used, so no need to demolish stack frame
	RET   8
ParseTempsFromString ENDP

; -----------------------------------------------------------------------------------------------------------
; Name: WriteTempsReverse
; Description: Prints the values of tempArray to the console in reverse order, separated by DELIMITER.
; Preconditions:	tempArray loaded with integer values in the same order as the file (incorrect order)
; Postconditions:	The values of tempArray, in reverse (corrected) order, printed to the console
; Receives:			[EBP+8]: OFFSET of tempArray
; Returns:			None
; -----------------------------------------------------------------------------------------------------------
WriteTempsReverse PROC
	PUSH  EBP
	MOV   EBP, ESP			; Establish base pointer

	PUSH  EAX				; Preserve registers used
	PUSH  EBX
	PUSH  ECX
	PUSH  EDX
	PUSH  ESI

	; Set ESI to point to the last SDWORD in the tempArray (add (4 bytes * TEMPS_PER_DAY) - 4 bytes)
	MOV   ESI, [EBP+8]
	MOV   EAX, TEMPS_PER_DAY
	MOV   EBX, 4
	MUL   EBX
	SUB   EAX, 4
	ADD   ESI, EAX

	; Set ECX to count how many times to loop
	MOV   ECX, TEMPS_PER_DAY

	; Print each integer from the tempArray, in reverse order
	_printVals:
		STD						; Set the direction flag to make sure the direction of movement is still
								; backwards. Used to set it outside _printVals, but it seems to get rest
								; within WriteInt
		LODSD					; Move the SDword to EAX, Decrement ESI by 4
		CALL  WriteInt

		; Print the delimiter character after each integer
		mDisplayChar DELIMITER
		LOOP  _printVals

	POP   ESI				; Restore registers used
	POP   EDX
	POP   ECX
	POP   EBX
	POP   EAX

	POP   EBP
	RET   4
WriteTempsReverse ENDP

END main