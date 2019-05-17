import zmq
import fnames

short_names = {
    fnames.IMAGE: 'im.json',
    fnames.TEXT: 'im.text',
    fnames.LINK: 'im.link'
}


def demonstration(port):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:{}".format(port))
    file_names = [fnames.IMAGE, fnames.LINK, fnames.TEXT]
    for name in file_names:
        socket.send_string('write {}'.format(short_names[name]))

        if socket.recv_string() == 'Ready!':

            with open(name, 'rb') as f:
                socket.send(f.read())

            if socket.recv_string() == 'Success!':
                print('{} was recorded!'.format(short_names[name]))

            else:
                print('Failed to record {}!'.format(short_names[name]))

    socket.send_string('dump')

    if socket.recv_string() == 'Success!':
        print('Dump file updated!')
    else:
        print('Failed to update dump file!')

    socket.send_string('read im.json')

    if socket.recv_string() == 'Success!':
        socket.send_string('Ready!')
        print('File {} received!'.format(short_names[name]))
        print('Content: ', end='')
        print(socket.recv_json())
