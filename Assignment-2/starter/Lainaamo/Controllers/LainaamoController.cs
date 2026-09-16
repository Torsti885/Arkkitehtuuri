using Microsoft.AspNetCore.Mvc;

namespace Lainaamo.Controllers;

[ApiController]
[Route("api")]
public class LainaamoController : ControllerBase
{
    private static readonly List<Item> _items = new()
    {
        new Item { Id = 1, Name = "Salibandymaila" },
        new Item { Id = 2, Name = "Projektori" },
        new Item { Id = 3, Name = "HDMI-kaapeli" }
    };

    private static readonly List<Loan> _loans = new()
    {
        new Loan { Id = 1, ItemId = 2, BorrowerName = "Aino", BorrowedAt = DateTime.UtcNow.AddDays(-3) },
        new Loan { Id = 2, ItemId = 3, BorrowerName = "Elias", BorrowedAt = DateTime.UtcNow.AddDays(-10), ReturnedAt = DateTime.UtcNow.AddDays(-8) }
    };

    private static int _nextItemId = 4;
    private static int _nextLoanId = 3;

    [HttpGet("items")]
    public IActionResult GetItems()
    {
        return Ok(_items);
    }

    [HttpPost("items")]
    public IActionResult CreateItem(Item item)
    {
        if (string.IsNullOrWhiteSpace(item.Name))
        {
            return BadRequest("Välineen nimi on pakollinen.");
        }

        item.Id = _nextItemId++;
        _items.Add(item);
        return Created($"/api/items/{item.Id}", item);
    }

    [HttpGet("loans")]
    public IActionResult GetLoans()
    {
        return Ok(_loans);
    }

    [HttpPost("loans")]
    public IActionResult Borrow(LoanRequest request)
    {
        Item? item = _items.FirstOrDefault(i => i.Id == request.ItemId);

        if (item == null)
        {
            return NotFound("Välinettä ei löydy.");
        }

        if (string.IsNullOrWhiteSpace(request.BorrowerName))
        {
            return BadRequest("Lainaajan nimi on pakollinen.");
        }

        if (_loans.Any(l => l.ItemId == request.ItemId && l.ReturnedAt is null))
        {
            return BadRequest("Väline on jo lainassa.");
        }

        Loan loan = new()
        {
            Id = _nextLoanId++,
            ItemId = request.ItemId,
            BorrowerName = request.BorrowerName,
            BorrowedAt = DateTime.UtcNow
        };
        _loans.Add(loan);
        return Created($"/api/loans/{loan.Id}", loan);
    }

    [HttpPost("loans/{id}/return")]
    public IActionResult ReturnLoan(int id)
    {
        Loan? loan = _loans.FirstOrDefault(l => l.Id == id);

        if (loan == null)
        {
            return NotFound("Lainaa ei löydy.");
        }

        if (loan.ReturnedAt is not null)
        {
            return BadRequest("Lainaa on jo palautettu.");
        }

        loan.ReturnedAt = DateTime.UtcNow;
        return Ok(loan);
    }
}

public class Item
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
}

public class Loan
{
    public int Id { get; set; }
    public int ItemId { get; set; }
    public string BorrowerName { get; set; } = string.Empty;
    public DateTime BorrowedAt { get; set; }
    public DateTime? ReturnedAt { get; set; }
}

public class LoanRequest
{
    public int ItemId { get; set; }
    public string BorrowerName { get; set; } = string.Empty;
}
