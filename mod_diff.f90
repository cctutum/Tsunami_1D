module mod_diff

    use iso_fortran_env, only: int32, real32
    implicit none
  
    private
    public :: diff_upwind, diff_centered
  
  contains
  
    pure function diff_centered(x) result(dx)
        ! Returns a 2nd order centered difference of a 1-d array,
        ! with periodic boundary condition.
        real(real32), intent(in) :: x(:)
        real(real32) :: dx(size(x))
        integer(int32) :: im
        im = size(x)
        dx(1) = x(2) - x(im)
        dx(im) = x(1) - x(im-1)
        dx(2:im-1) = x(3:im) - x(1:im-2) ! dx(i) = (x(i+1)-x(i-1))/2
        dx = 0.5 * dx
        ! Here, we multiply with 0.5 instead of dividing by 2,
        ! because for floating-point (real) numbers, multiplication 
        ! is a much faster operation than division.
    end function diff_centered
  
  
    pure function diff_upwind(x) result(dx)
        ! Returns a 1st-order upstream finite difference of a 1-d array,
        ! with periodic boundary condition.
        real(real32), intent(in) :: x(:)
        real(real32) :: dx(size(x))
        integer(int32) :: im
        im = size(x)
        dx(1) = x(1) - x(im)
        dx(2:im) = x(2:im) - x(1:im-1)
    end function diff_upwind
  
  end module mod_diff