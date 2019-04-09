from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {'boards':boards}
    return render(request, 'boards/index.html', context)

@login_required
def create(request):
    # post 요청이면 form데이터를 처리한다.
    if request.method == "POST":
        #  이 처리 과정은 'binding'이라고 불리는데, 폼의 유효성 체크를 할 수 있도록 해준다.
        form = BoardForm(request.POST)
        # form 유효성 체크
        if form.is_valid():
        # cleaned_data : 유효성검증을 위한 것.
            board = form.save(commit=False) # board를 바로 저장하지 않는다는 것.
            board.user = request.user
            board.save()
            return redirect('boards:detail', board.pk)
            # title = form.cleaned_data.get('title')
            # content = form.cleaned_data.get('content')
            # # 검증을 통과한 데이터로 보드를 만든다.
            # board = Board.objects.create(title=title, content=content)
            # return redirect('boards:detail', board.pk)
    # post가 아닌 요청이면 기본 폼을 생성한다.
    else:
        form = BoardForm()
    context = {'form':form}
    return render(request, 'boards/form.html', context)
        
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    context = {'board':board}
    return render(request, 'boards/detail.html', context)
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == "POST":
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')

@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == "POST":
            form = BoardForm(request.POST, instance=board)
            if form.is_valid():
                board = form.save()
                return redirect('boards:detail', board.pk)
        # get 요청이면(혹은 수정하기 버튼을 눌렀을 떄)
        else:
            
            # 원래는 이렇게 써야 함
            # form = BoardForm(initial={'title' : board.title, 'content':board.content})
            # boardForm을 초기화(사용자 입력 값을 넣어준 상태로)
            # form 
            form = BoardForm(instance=board)
    else:
        return redirect('boards:index')
    context = {'form' : form, 'board':board}
    # POST :  요청에서 검증에 실패하였을때, 오류메시지가 포함된 상태
    # GET : 요청에서 초기화 된 상태.
    return render(request, 'boards/form.html', context)